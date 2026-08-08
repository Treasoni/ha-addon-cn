# haos-mirror-switcher 0.2.2 探测失败研究

日期：2026-08-08
范围：只读资料调查与本地代码审阅，不包含代码、配置或 workflow 修改。
研究问题：为什么点击“立即检查”后得到“镜像源探测失败：无法生成完整探测结果”，以及 Docker Registry pull-through mirror、Home Assistant Supervisor 的实际行为应如何被探测和配置。

## 结论先行

1. 当前 0.2.2 的直接故障是本地状态读取函数把带点的 registry 主机名当成了嵌套路径。enabled.ghcr.io 被拆成 enabled -> ghcr -> io，而状态文件中的真实键是 enabled["ghcr.io"]。三个仓库因此都走“未启用”分支，只输出 RECOMMENDED、不输出任何 RESULT；随后完整性校验主动失败，Web API 再把它映射成通用的“请稍后重试”。这是当前按钮不可用的确定根因。
2. “全部候选不可用”应是一次成功完成但没有可用推荐的业务结果，不应和 JSON 损坏、聚合器崩溃混为“探测器内部失败”。当前代码的完整性校验过于严格，且没有把“无候选”和“全部失败”展示给用户。
3. 当前官方 Supervisor 源码没有 registries_mirror 配置字段或对应 REST 配置接口。Supervisor 的 docker.json 是 Supervisor 自己的数据文件，当前官方 schema 只处理 registry 凭据、IPv6 和 MTU；它不是 Docker daemon 的镜像源配置文件。向其中写入 registries_mirror 不属于官方接口。
4. Docker 官方文档规定 Docker Hub pull-through mirror 使用 Docker daemon 的 registry-mirrors，持久化位置是 /etc/docker/daemon.json，修改后要 reload Docker。HAOS 官方源码也提供了 /etc/docker/daemon.json 并由 dockerd 服务读取。仅重启 Supervisor 不足以使 daemon 镜像配置生效。
5. Supervisor 看到 ghcr.nju.edu.cn 的一次 404 后仍然成功拉取 add-on，并不矛盾：当前 Supervisor 为进度统计做的 manifest 预取是可选的，而且认证预检查固定请求同一仓库的 latest，并不等于随后真正拉取的版本 tag。预检查失败后仍会继续 Docker pull。
6. “真实 manifest 探测”方向是正确的，但必须探测与实际 pull 一致的 repository/tag、接受正确的 manifest media type，并区分 200、认证挑战、目标不存在、网络超时和代理协议不兼容。不能把任意 401 当成“该 tag 可用”。

## 资料范围与访问备注

仓库没有现成的 docs/research/ 研究记录目录；已有记录主要是 docs/adr/，因此按用户指定的回退路径新增本文件。

本次只使用以下一手资料类别：

- Docker Distribution Registry HTTP API V2 规范；
- Docker 官方 Docker Hub pull-through mirror 文档；
- Home Assistant Supervisor 官方仓库源码；
- Home Assistant Operating System 官方仓库源码；
- Home Assistant add-on/app 官方配置文档。

官方开发者文档的 raw Markdown 地址返回 404，但官方 HTML 页面可访问并包含同一配置表；研究引用使用该 HTML URL。HAOS 仓库在 Windows checkout 时有一个包含特殊转义字符的路径无法落盘，但 Git 对象可通过 git show / git grep 读取；这不影响对 daemon.json 和 systemd unit 的核验。没有因页面读取困难而转用博客、论坛或搜索摘要。

源码基线：

- Supervisor：64961ef9d19e934594746b551201b1922f5a4ea3，2026-08-04；
- Home Assistant Operating System：6930145f9692258ba5b9e67c3bf250652777b466，2026-08-06。

## 一、当前 0.2.2 报错的本地因果链

### 1. 点号键路径导致三个 registry 都被当成未启用

来源 URL：本仓库本地实现
相关文件/方法：C:\homeassistant\haos-mirror-switcher\lib\actions.sh，_state_field() 第 124-148 行，probe_all() 第 396-418 行。
结论：_state_field() 执行 sys.argv[1].split(".")。probe_all() 用 _state_field "enabled.$reg" 读取 ghcr.io、docker.io、lscr.io，所以实际查找的是：

~~~text
enabled -> ghcr -> io
enabled -> docker -> io
enabled -> lscr -> io
~~~

但 ensure_state() 写入的结构是：

~~~json
{
  "enabled": {
    "ghcr.io": true,
    "docker.io": true,
    "lscr.io": true
  }
}
~~~

查找不到三级路径时函数输出空字符串；空字符串不等于 true，于是三个 registry 都直接输出空的 RECOMMENDED，跳过候选源循环和 RESULT 输出。

对当前修复方案的影响：这是 P0 确定性修复。读取带点主机名必须使用 JSON 的键访问，不能用点分隔路径；应为此增加回归测试，至少覆盖 ghcr.io、docker.io、lscr.io 三个键。

### 2. 没有 RESULT 后被误报为“无法生成完整探测结果”

来源 URL：本仓库本地实现
相关文件/方法：C:\homeassistant\haos-mirror-switcher\lib\actions.sh，probe_all() 第 419-480 行；C:\homeassistant\haos-mirror-switcher\server.py，do_POST() 中 /api/probe 第 260-271 行。
结论：聚合 Python 代码只在收到 RESULT 行时填充 probe_results。由于上一节的分支没有 RESULT，结果类似于：

~~~json
{
  "probe_results": {},
  "recommended": {
    "ghcr.io": null,
    "docker.io": null,
    "lscr.io": null
  }
}
~~~

当前校验要求 probe_results 是非空字典；校验失败就记录“镜像源探测失败：无法生成完整探测结果”并返回失败。服务端把非零退出统一返回 PROBE_FAILED 与“镜像源检查失败，请稍后重试”。前端没有推荐源时自然禁用“应用推荐配置”。

对当前修复方案的影响：应分成两个结果：

- PROBE_RESULT_INVALID：聚合器崩溃、JSON 损坏、缺少必需字段、状态无法安全写回；
- PROBE_COMPLETED_NO_USABLE_SOURCE：每个启用的 registry 都已经探测，但没有候选返回可用 manifest。

第二种结果应保留每个 registry、每个候选的状态，当前配置不变，按钮继续不可用，但页面应明确显示“检查完成，暂时没有可用源”，而不是要求用户盲目刷新。

### 3. 现有 probe_host 的状态分类仍需收紧

来源 URL：本仓库本地实现
相关文件/方法：C:\homeassistant\haos-mirror-switcher\lib\actions.sh，probe_host() 第 279-348 行。
结论：当前探测使用真实 manifest GET：

~~~text
GET https://<host>/v2/<repository>/manifests/<tag>
~~~

200 只有在 Content-Type 看起来像 manifest/JSON 且响应 JSON 含 manifest 相关字段时才记为成功；401 无论是否存在完整 WWW-Authenticate 都记为 ok:401；其他状态和 curl 无响应都记为失败。

对当前修复方案的影响：401 应至少记录为“registry 可达但需要认证”，不能直接作为无认证情况下可推荐的镜像源。除非完成 WWW-Authenticate 解析、token 请求并用同一个 repository/tag 重试，否则只能证明 API 入口可达，不能证明目标镜像可拉取。

## 二、Docker Registry V2 manifest GET/HEAD 语义

### 1. API 规范

来源 URL：<https://distribution.github.io/distribution/spec/api/>
相关章节/方法：GET /v2/<name>/manifests/<reference>，HEAD /v2/<name>/manifests/<reference>，GET /v2/ API version check。
结论与影响如下：

| 响应 | 规范语义 | 对探测器的处理 |
|---|---|---|
| GET 200 | 指定 repository 与 tag/digest 的 manifest 成功返回；响应 Content-Type 指示 manifest 类型，客户端应声明支持的 media type。 | 可以作为“目标存在”的候选成功，但仍应解析 JSON/manifest 结构。 |
| HEAD 200 | 指定 manifest 存在；返回 Content-Length、Docker-Content-Digest 等头，不返回 body。 | 可以作为存在性检查；不能依赖 body 校验。对代理兼容性不确定时可用 GET 作为回退。 |
| GET 或 HEAD 401 | 需要按 WWW-Authenticate 内容采取认证动作并重试；这是认证控制结果。 | 证明入口响应了 Registry API，但不单独证明匿名 pull 或指定 tag 可用。记录为 AUTH_REQUIRED，不要直接推荐。 |
| GET 或 HEAD 404 | 对 manifest endpoint 表示该 registry 不知道指定 image/manifest；对 /v2/ version check 的 404 则表示客户端不应假定服务实现了 V2。 | 真实目标的 404 应记为 TARGET_NOT_FOUND；它不是 DNS/TLS 超时，也不能单独证明主机完全不可达。 |
| 超时、DNS/TLS/连接错误 | 没有形成 HTTP 响应，因此不存在 Registry API 状态语义。 | 记为 SOURCE_UNREACHABLE，标记可重试，并保留具体阶段（DNS、TLS、connect、read、deadline）。 |

对本项目最重要的边界是：/v2/ 返回 200/401 只能做 API 入口健康检查；要推荐一个镜像源，必须对确定的真实 repository/tag 做 manifest GET 或 HEAD。tags/list、latest 或只访问 /v2/ 都不能替代这个检查。

### 2. 真实 manifest 的 media type 与路径

来源 URL：<https://distribution.github.io/distribution/spec/api/>
相关章节/方法：manifest endpoint 的 Accept 要求、manifest response Content-Type、manifest body。
结论：客户端应在请求中声明支持的 manifest 类型，成功响应的 Content-Type 才是实际返回类型。多架构镜像可能先返回 image index/manifest list，再按平台选择子 manifest。

对当前修复方案的影响：

- 候选配置必须按 registry 使用真实、长期存在的 repository/tag；
- Docker Hub 官方镜像要使用规范的 library/<image> 命名，例如 library/alpine，不能把短名和完整名混用；
- 请求的 Accept 至少应覆盖 Docker schema 2、OCI manifest、Docker manifest list、OCI image index；
- 200 但返回 HTML、登录页、网关错误页或不可解析 JSON，必须拒绝；
- 404、401、超时必须分别展示，不能只显示“检查失败”。

## 三、为什么 Supervisor 预检 404 后仍可能实际 pull 成功

### 1. 官方 Supervisor 的预取是可选的

来源 URL：<https://github.com/home-assistant/supervisor/blob/64961ef9d19e934594746b551201b1922f5a4ea3/supervisor/docker/interface.py#L289-L325>
相关源码方法：DockerInterface.install()。
结论：Supervisor 在真正 pull_image() 前，先调用 manifest_fetcher.get_manifest() 获取层大小，用于更准确的进度显示。源码明确将其标记为 optional；manifest 失败只回退到按数量统计的进度，不应阻止后续 pull。

对当前修复方案的影响：看到“Failed to fetch manifest”或“Unexpected status”不能直接判断 add-on 安装失败；应继续观察后面的 Downloading docker image、successfully installed 或真正的 pull 错误。

### 2. 预检的第一次请求固定使用 latest

来源 URL：<https://github.com/home-assistant/supervisor/blob/64961ef9d19e934594746b551201b1922f5a4ea3/supervisor/docker/manifest.py#L108-L160>
相关源码方法：RegistryManifestFetcher._get_auth_token()。
结论：为了发现认证方式，Supervisor 对当前 repository 先请求：

~~~text
GET https://<api-endpoint>/v2/<repository>/manifests/latest
~~~

如果不是 200 或 401（包括 404），源码记录 Unexpected status 并返回无 token；之后仍会继续获取真正版本的 manifest。

来源 URL：<https://github.com/home-assistant/supervisor/blob/64961ef9d19e934594746b551201b1922f5a4ea3/supervisor/docker/manifest.py#L191-L284>
相关源码方法：RegistryManifestFetcher._fetch_manifest()、get_manifest()。
结论：真正的 manifest 请求使用调用方传入的 tag，并带完整 Accept 列表。它与前面的 latest 不是同一个 reference。

对当前修复方案的影响：如果 pull-through 入口没有 latest，或者其缓存只保留实际发布的版本 tag，Supervisor 日志出现一次 404 但之后指定版本 pull 成功是合理的。镜像探测器不应照抄这个 latest 预检；必须固定使用确实要拉取的版本 tag。当前用户日志中“ghcr.nju.edu.cn 预检 404，随后 0.2.2 安装成功”与这条源码路径一致。

## 四、Supervisor 的 docker.json 与 registries_mirror 配置边界

### 1. 官方 Supervisor 当前没有 registries_mirror 字段

来源 URL：<https://github.com/home-assistant/supervisor/blob/64961ef9d19e934594746b551201b1922f5a4ea3/supervisor/const.py#L31-L41>
相关源码常量：FILE_HASSIO_DOCKER。
结论：Supervisor 的 Docker 配置文件路径是：

~~~text
/data/docker.json
~~~

在 HAOS 中，Supervisor 容器内的 /data 对应其 Supervisor 数据目录；它是 Supervisor 配置数据文件，不等于宿主机 Docker daemon 的 /etc/docker/daemon.json。

来源 URL：<https://github.com/home-assistant/supervisor/blob/64961ef9d19e934594746b551201b1922f5a4ea3/supervisor/docker/manager.py#L206-L241>
相关源码类/方法：DockerConfig、DockerAPI.post_init()。
结论：DockerConfig 当前公开的配置属性是 enable_ipv6、mtu、registries（registry 凭据）；启动初始化时读取 FILE_HASSIO_DOCKER。源码中没有 registries_mirror 属性。

来源 URL：<https://github.com/home-assistant/supervisor/blob/64961ef9d19e934594746b551201b1922f5a4ea3/supervisor/validate.py#L240-L253>
相关源码 schema：SCHEMA_DOCKER_CONFIG。
结论：当前 schema 只定义：

- registries：每个 registry 的 username/password；
- enable_ipv6；
- mtu。

没有 registries_mirror。本次对已完整获取的 Supervisor Git 历史执行了 -Sregistries_mirror 与 -Sregistry-mirrors 搜索，也没有找到该字段；因此不能把它当作官方 Supervisor 接口或稳定兼容字段。

来源 URL：<https://github.com/home-assistant/supervisor/blob/64961ef9d19e934594746b551201b1922f5a4ea3/supervisor/utils/common.py#L88-L113>
相关源码方法：FileConfiguration.read_data()。
结论：文件读入后会按 schema 校验；校验失败会记录 critical、警告 Resetting ... to default，并在内存中恢复默认配置。

对当前修复方案的影响：当前 haos-mirror-switcher 的 build_target() 把 registries_mirror 合并写入 /data/docker.json，再调用 Supervisor restart。这条链路没有官方实现依据，可能导致 Supervisor 将文件视为非法配置并在内存中重置，而且不会配置 Docker daemon 的镜像源。当前 ADR/README 中“管理 Supervisor 的 registries_mirror”需要先暂停为正式承诺，不能只修探测器后继续保留“应用成功即可生效”的文案。

### 2. 官方 Supervisor API 也没有镜像源写入接口

来源 URL：<https://github.com/home-assistant/supervisor/blob/64961ef9d19e934594746b551201b1922f5a4ea3/supervisor/api/docker.py#L28-L127>
相关源码类/方法：APIDocker.info()、options()、registries()、create_registry()、remove_registry()。
结论：官方 Docker API 只提供 IPv6、MTU 以及 registry 凭据管理；options() 变更 IPv6/MTU 时还会记录需要主机重启的 resolution issue。没有镜像 mirror 的配置字段或对应写入方法。

对当前修复方案的影响：不能通过 Supervisor REST API 猜测或补写 registries_mirror。若要支持宿主 Docker daemon 的 registry mirror，必须找到并验证目标 HAOS 版本上真实存在的官方/系统级配置入口；在找到之前，“应用推荐配置”不应声称已经改变 Supervisor 的实际拉取路径。

### 3. docker_api 与保护模式的官方边界

来源 URL：<https://developers.home-assistant.io/docs/add-ons/configuration/>
相关配置项：docker_api、image、ingress。
结论：官方 add-on/app 配置文档将 docker_api 描述为只读 Docker API 访问，并说明只对未保护的 app 生效。当前 Supervisor 源码中，MOUNT_DOCKER 将 /run/docker.sock 以 read_only=True 挂载，且只有 not protected 且声明了 docker_api 才加入该挂载：

- <https://github.com/home-assistant/supervisor/blob/64961ef9d19e934594746b551201b1922f5a4ea3/supervisor/apps/model.py#L391-L393>：App.access_docker_api；
- <https://github.com/home-assistant/supervisor/blob/64961ef9d19e934594746b551201b1922f5a4ea3/supervisor/docker/const.py#L169-L174>：MOUNT_DOCKER；
- <https://github.com/home-assistant/supervisor/blob/64961ef9d19e934594746b551201b1922f5a4ea3/supervisor/docker/app.py#L619-L622>：挂载条件。

对当前修复方案的影响：用户关闭保护模式后看到 socket 是符合官方挂载条件的；但 add-on API 权限文档并不承诺可以用 docker cp 修改 hassio_supervisor 容器中的 Supervisor 配置。此前“docker cp 失败，写回滚”应作为权限/写入边界问题单独诊断，不能用“重启加载项”掩盖。

## 五、Docker pull-through mirror 的官方语义与陷阱

### 1. 只定义 Docker Hub mirror，不是所有 registry 的通用重写

来源 URL：<https://docs.docker.com/docker-hub/image-library/mirror.md>
相关章节：Gotcha、How does it work?、Configure the Docker daemon。
结论：Docker 官方文档明确写出目前不能 mirror 另一个 private registry，只有 central Docker Hub 可被 mirror。pull-through cache 会响应普通 Docker pull 请求，并把内容存到本地；首次请求会从公共 Docker registry 拉取并缓存，后续请求再从缓存服务。

官方 daemon 配置示例是：

~~~json
{
    "registry-mirrors": ["https://<my-docker-mirror-host>"]
}
~~~

持久化文件是 /etc/docker/daemon.json，保存后 reload Docker 才会生效。

对当前修复方案的影响：

- docker.io 可以按 Docker daemon 的 registry-mirrors 语义设计，但不能把这个配置泛化为 ghcr.io、lscr.io；
- GHCR/LSCR 若要国内入口，应采用实际 image 名称重写、分别兼容的 registry proxy，或项目自己发布的预构建镜像；不能仅写一个 Docker Hub mirror 数组；
- 首次冷缓存可能需要访问上游并耗时较长，8 秒探测超时不能直接等同于镜像站永久不可用；
- 一个 pull-through host 的可达性不等于它已具备某个具体 repository/tag，仍必须探测真实 manifest 并最终验证实际 pull。

### 2. 真实 repository/tag、认证与 media type 是三类独立兼容条件

来源 URL：<https://distribution.github.io/distribution/spec/api/>
相关章节：Pulling an Image Manifest、Existing Manifests、API Version Check、错误码表。
结论：

- 代理必须正确转发 /v2/<name>/manifests/<reference>，其中 <name> 与 <reference> 必须保留；
- Docker Hub 官方镜像的 <name> 是 library/<image> 这类完整 namespace；
- 代理若只实现 /v2/ 或 tags/list，不能视为支持真实 pull；
- 代理若只支持某一种 schema，而探测器的 Accept 或 Docker daemon 的 Accept 包含 OCI index/manifest list，可能出现 406、404 或错误内容；
- 代理返回 401 时，必须转发完整 WWW-Authenticate 并允许 token 流程；简单把 401 记为成功会把需要登录、错误 scope、公共代理认证页都误判为可用；
- 代理返回 200 但 body 是 HTML 登录页或网关提示页，仍然不是 manifest；
- 代理对 HEAD 和 GET 的实现可能不一致。规范定义 HEAD 用于不返回 body 的存在性检查，因此探测器应在实际 pull 兼容性优先时使用 GET，并校验 JSON 与 Content-Type；若采用 HEAD，应额外测试 Docker daemon 的真实 HEAD/GET 行为。

对当前修复方案的影响：候选源白名单应保存真实探测 fixture（repository/tag/media type/期望架构），而不是只保存 host。探测结果应至少包含 HTTP 状态、耗时、最终 URL/重定向信息、Content-Type、解析结果和可重试性。

## 六、对“全部候选不可用”的分类判断

来源 URL：Docker Registry API 规范（HTTP 状态和 manifest error 语义）
<https://distribution.github.io/distribution/spec/api/>
相关本地方法：C:\homeassistant\haos-mirror-switcher\lib\actions.sh 的 probe_host()、probe_all()。
结论：候选循环只要完整执行完，并且每个候选都有明确的 200/401/404/超时/连接错误结果，即使没有任何可推荐源，探测器也已经完成了它的工作。这是业务结果“无可用源”，不是内部异常。

真正的内部失败包括：

- Python 聚合器异常退出；
- RESULT 行格式损坏或包含无法解析的分隔符；
- /data/probe_out.json 不是合法 JSON；
- 缺少 probe_results、recommended、探测时间等必需结构；
- 状态文件无法原子写回。

对当前修复方案的影响：

1. 每个 registry 都必须有一个结果对象，即使候选清单为空；
2. 每个候选无论成功或失败都必须被记录；
3. recommended 为空只能让“应用推荐配置”保持禁用，不能让整个 /api/probe 变成服务器错误；
4. UI 应显示“检查已完成，但没有可用镜像源”，并展示最短可行动建议（稍后重试、检查网络、在高级区添加已知源）；
5. 只有聚合/持久化失败才返回 PROBE_RESULT_INVALID，并把诊断信息写入日志。

## 七、修复规划与实施结果

### P0-A：先修当前按钮不可用

1. 修复 registry 键访问：禁止把主机名放进点分隔状态路径；使用结构化 JSON 读取或对键进行明确转义。
2. 保留三个 registry 的完整行：disabled、no_candidate、候选逐项 RESULT、最终 recommended。
3. 增加可观测字段：探测开始/结束时间、候选 host、repository、tag、HTTP 状态、错误阶段、重试建议。
4. 将日志/API/UI 错误码分为：
   - PROBE_COMPLETED_WITH_RECOMMENDATION；
   - PROBE_COMPLETED_NO_USABLE_SOURCE；
   - PROBE_SOURCE_UNREACHABLE；
   - PROBE_TARGET_NOT_FOUND；
   - PROBE_AUTH_REQUIRED；
   - PROBE_RESULT_INVALID。
5. 401 仅在完成认证挑战并用同一 repository/tag 成功重试后才能升级为可推荐；否则展示“源可达，但需要认证”。

### P0-B：重新定义“应用配置”的真实边界

当前资料不支持继续把“向 /data/docker.json 写入 registries_mirror + 重启 Supervisor”作为通用 HAOS 解决方案。实现前必须在以下方案中做出可验证选择：

- 推荐方案：对自有 add-on 使用国内预构建入口或直接改写实际 image host；对 Docker Hub、GHCR、LSCR 分别验证真实 pull，不伪装成一个通用 mirror；
- 受限方案：如果只支持 Docker Hub mirror，目标必须是 HAOS 宿主的 /etc/docker/daemon.json 的 registry-mirrors，并执行/触发 Docker daemon reload/restart；需要单独验证目标 HAOS 版本、权限、回滚和系统更新后的持久性；
- 不推荐继续保留的方案：写 Supervisor /data/docker.json 的非官方 registries_mirror 字段，再只重启 Supervisor。

在 P0-B 完成前，Web 界面应把“应用推荐配置”标为未支持/未验证，或只允许执行已经证明会改变 daemon 实际行为的路径；不能显示“应用成功”后让用户误以为所有 Supervisor 拉取都已走代理。

### P1：把探测从“可达”升级为“可拉取”

对每个候选源使用与目标 pull 一致的真实 fixture：

~~~text
registry host + repository + version tag + Accept + expected architecture
~~~

探测完成后至少验证一次真实 pull 或等价的 manifest/子 manifest 解析；尤其验证：

- ghcr.io 的真实 image path；
- docker.io 的 library/<name>；
- 多架构 index 是否含 amd64 / arm64；
- 401 的 token challenge；
- 200 的 JSON 和 Content-Type；
- 404 与非 manifest HTML；
- 冷缓存延迟、DNS、TLS、连接超时。

### P1：小白 UI 的结果设计

- 成功且有推荐：显示“已找到可用源”，展示将要改变的 registry 和 host；
- 完成但无推荐：显示“检查完成，当前没有可用源”，按钮保持禁用；
- 入口可达但需认证：显示“源需要认证，暂不自动应用”；
- 聚合器异常：显示“程序没有生成完整结果”，提供日志中的错误码；
- 应用失败：显示实际写入位置、是否已回滚、是否需要重启 Docker daemon，而不是只说“请重试”。

## 八、验证矩阵与成功标准

### 探测器回归测试

| 场景 | 预期分类 | 预期副作用 |
|---|---|---|
| enabled["ghcr.io"] == true | 真正执行 ghcr 候选探测 | 产生 RESULT，不再因点号键跳过 |
| 所有候选超时 | PROBE_COMPLETED_NO_USABLE_SOURCE + SOURCE_UNREACHABLE 明细 | 不修改现有配置 |
| 所有候选 404 | PROBE_COMPLETED_NO_USABLE_SOURCE + TARGET_NOT_FOUND 明细 | 不修改现有配置 |
| 无候选 | PROBE_COMPLETED_NO_USABLE_SOURCE + NO_CANDIDATE | 不修改现有配置 |
| 一个候选 200、其余失败 | 成功完成并推荐 200 候选 | 只有用户确认后才应用 |
| 401 无认证 | PROBE_AUTH_REQUIRED | 不直接推荐 |
| 聚合 JSON 损坏 | PROBE_RESULT_INVALID | 不覆盖旧状态、不修改 Docker |
| registry 主机名含点号/端口 | 正确按完整 JSON key 读取 | 有专门回归测试 |

### 配置与实际拉取验证

1. 证明写入的是 Docker daemon 实际读取的配置文件，而不是只证明 Supervisor 容器内某个 JSON 被改动。
2. 若采用 Docker Hub mirror，确认 /etc/docker/daemon.json 的 registry-mirrors 结构、Docker daemon reload/restart、docker info 的 mirror 列表和一次真实 docker pull。
3. 若采用 GHCR/LSCR 国内入口，确认最终 image reference 已重写到实际支持的 host，并在对应真实 tag 上验证 manifest 和 pull；不能用 Docker Hub 的 registry-mirrors 结论替代。
4. 复现 Supervisor 的 latest 预检 404 + 指定 tag pull 成功，确保日志提示不会被误读为安装失败。
5. 在写入失败、daemon 重启失败、探测全失败三种情况下，确认原配置保持不变，并能从 UI 看见明确错误码。

## 九、对当前仓库文档/ADR 的影响

来源 URL：本仓库现有文档
相关文件：C:\homeassistant\docs\adr\0005-domestic-prebuilt-entry-and-key-path.md 第 11-17 行、C:\homeassistant\CONTEXT.md 第 45-57 行、C:\homeassistant\haos-mirror-switcher\README.md 第 12-16、26、51-53 行。
结论：仓库已经正确区分“预构建镜像入口”和“运行时镜像源”，但仍把 registries_mirror 当成可由加载项管理的 Supervisor 配置。

对当前修复方案的影响：下一轮实现前应先更新领域约定/ADR，明确：

- 预构建入口：解决本加载项首次安装；
- Docker Hub daemon mirror：只解决 Docker Hub，且需要 daemon 的真实配置入口；
- GHCR/LSCR：需要实际 image host 重写或各自代理，不等同于 Docker Hub mirror；
- 下载代理：只用于 OTA/HACS 运行时下载；
- “关键路径国内可用”：必须以实际安装/pull 结果定义，不以写入某个 JSON 文件定义。

## 参考资料索引

1. Docker Distribution Registry HTTP API V2：<https://distribution.github.io/distribution/spec/api/>
2. Docker 官方 Docker Hub pull-through mirror：<https://docs.docker.com/docker-hub/image-library/mirror.md>
3. Home Assistant Supervisor 官方源码基线：<https://github.com/home-assistant/supervisor/tree/64961ef9d19e934594746b551201b1922f5a4ea3>
4. Supervisor Docker 配置 schema：<https://github.com/home-assistant/supervisor/blob/64961ef9d19e934594746b551201b1922f5a4ea3/supervisor/validate.py#L240-L253>
5. Supervisor manifest fetcher：<https://github.com/home-assistant/supervisor/blob/64961ef9d19e934594746b551201b1922f5a4ea3/supervisor/docker/manifest.py>
6. Home Assistant Operating System Docker daemon 配置：<https://github.com/home-assistant/operating-system/blob/6930145f9692258ba5b9e67c3bf250652777b466/buildroot-external/rootfs-overlay/etc/docker/daemon.json>
7. Home Assistant Operating System Docker service：<https://github.com/home-assistant/operating-system/blob/6930145f9692258ba5b9e67c3bf250652777b466/buildroot-external/rootfs-overlay/usr/lib/systemd/system/docker.service.d/haos.conf>
8. Home Assistant add-on/app 配置文档：<https://developers.home-assistant.io/docs/add-ons/configuration/>

## 十、实施记录（0.2.3）

- 状态读取改为传递独立路径段：`enabled` 与 `ghcr.io`、`docker.io`、`lscr.io` 不再经过点号拆分，因此主机名始终作为完整 JSON key 读取。
- 探测聚合为三个 registry 预建结果对象，并以完成标记区分“完整检查但没有可用候选”和“聚合过程异常”。前者保留现有配置并返回成功检查状态，后者仍返回失败。
- Ingress API 对无推荐结果返回 `PROBE_COMPLETED_NO_RECOMMENDATION`，提示用户当前配置未改动且可稍后重试；页面不会再显示笼统的内部失败。
- 已加入 `ghcr.io`、`docker.io`、`lscr.io` 带点键读取回归测试，以及无可用候选时的 API 状态测试。

0.2.4 已实施 P0-B 的安全决策：`apply` 与自动维护不再写入 Supervisor 的
`registries_mirror`，Web 界面停用应用按钮；仅保留用户明确触发的旧配置清理，
并增加读取、写入、读回校验和回滚检查。该版本不再宣称运行时可以一键切换
HAOS 的全局镜像源。
