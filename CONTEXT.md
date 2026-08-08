# ha-addon-cn 领域术语

本仓库是一个 Home Assistant Add-on 中文商店：仓库根目录即商店，子目录是各个 add-on，`README.md` 即中文使用指南。

## Language

**add-on 商店**：
由 `repository.json` 描述的 Home Assistant Add-on 仓库；根目录下的 `{slug}/` 是一个 add-on。

_Avoid_: 插件库、仓库商店

**vendored add-on**：
从上游镜像到本仓库的 add-on，`source` 为 `alexbelgium`、`official` 或 `frenck`。同步脚本可以更新其 README 之外的文件。

_Avoid_: 上游插件、第三方插件

**source: local**：
仓库自行维护的 add-on。同步脚本不会修改或删除这类 add-on。

_Avoid_: 自建插件、本地插件

**中文指南**：
add-on 的 `README.md` 本身就是中文使用指南，通过首部标记识别，由 Home Assistant 详情页直接渲染。

_Avoid_: README_zh、中文说明文件

**审校**：
审校代理依据 add-on 配置声明核对中文 README 的语义准确性，并在需要时修复并留下学习记录。

_Avoid_: 校对、复稿、审核

**结构门禁**：
针对中文 README 的确定性校验，是质量控制与复验使用的第一道关卡。

_Avoid_: lint、静态检查

**desync**：
磁盘 README 已有中文指南标记，但商店清单仍标示缺失的不同步状态。此时只修正标记，不重写 README。

_Avoid_: 不同步、漂移

**质量维度**：
工作流强制校验的两个维度：结构规范（章节、标记和命名）与事实准确（配置项、命令、端口和链接真实对应）。

_Avoid_: 质量标准、规范

**镜像地址重写（image rewrite）**：
以脚本化且幂等的方式修改 add-on `config.yaml` 中 `image:` 的 registry 主机名，同时保留路径与 `{arch}` 占位符。

_Avoid_: 换源、改镜像、本地化镜像

**镜像源 / registry proxy**：
代理容器镜像 registry 的服务，例如用于转发 `ghcr.io` 的镜像站。它不同于完整镜像仓库，也不同于 Docker Hub 的 daemon 镜像加速配置。

_Avoid_: 加速器、Docker 镜像加速

**镜像源探测完成**：
候选源检查已形成业务结果。即使没有可用候选源，也属于完成；现有配置必须保持不变。只有探测过程未能完成才是探测失败。

_Avoid_: 没有推荐源等同于探测器错误

**同步后变换（post-sync transform）**：
同步管道在复制上游文件后立即执行的幂等变换。先变换再比较，可防止下次同步覆盖本地规则，并避免误报更新。

_Avoid_: 同步钩子、改写步骤

**上游资料卡**：
自有 add-on 的 `config.yaml` 顶部注释块，记录上游软件端口、默认凭据、数据目录、环境变量与版本。先收集资料再编写是强制要求。

_Avoid_: 需求文档、开发笔记

> “镜像”三义：**镜像仓库**（vendored add-on 的代码副本）、**镜像源**（registry proxy）和 **镜像地址重写**（修改 `image:` 字段）。应按语境区分。
