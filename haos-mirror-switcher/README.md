<!-- zh-guide -->
# HAOS 国内换源

这是一个面向 Home Assistant OS（HAOS）`amd64` / `aarch64` 的国内网络检查与恢复工具。它可以检查候选镜像入口，并清理旧版本留下的非官方镜像映射；它不会声称能够通过 Supervisor 内部文件直接改变 HAOS 的全局拉取源。

## 简介

国内网络下，Home Assistant 常见的卡点有三种，含义并不一样：

| 名称 | 用途 | 本加载项是否负责 |
|---|---|---|
| 镜像入口 | 首次安装本加载项时，Supervisor 从哪里拉预构建镜像 | 是，使用 `ghcr.nju.edu.cn` 国内入口 |
| 镜像源 | Supervisor 拉取 `ghcr.io`、`docker.io`、`lscr.io` 容器镜像时使用的代理 | 仅检查；本加载项不写入全局配置 |
| 下载代理 | OTA 或 HACS 运行时下载 GitHub 内容的中转地址 | 仅 OTA 实验功能使用 |

“国内关键路径可用”表示首次安装、换源和 HACS 安装不要求用户直连 GitHub、GHCR 或 `get.hacs.vip`；不表示所有公益代理永久稳定，也不提供 SLA。

## 安装

推荐顺序是：先确保 Supervisor 可以安装普通加载项，再安装并运行 `hacs-cn-install`。本加载项不能替代 HAOS 的官方 Docker 网络配置。

1. 在 Home Assistant → 设置 → 加载项 → 商店 → 右上角菜单，添加商店仓库：
   - Gitee：<https://gitee.com/zhqznc_10603234_123/ha-addon>
   - GitHub：<https://github.com/Treasoni/ha-addon-cn>
2. 搜索“HAOS 国内换源”，安装并启动。
3. 安装完成后，在加载项页面关闭“保护模式（Protection mode）”，再启动加载项。这个权限只用于读取状态，以及在你明确点击恢复按钮时清理旧版本配置。
4. 点击“打开 Web 界面”。本加载项使用国内预构建入口，不需要你先配置 Docker Hub 或 GHCR 的本地构建通道。

如果商店仓库可达但预构建镜像入口暂时不可用，请稍后重试；国内 pull-through 镜像站是公益服务，可能临时失效。

## 配置

普通用户可以保留默认值。首次启动和周期检查都只读，不会改写 Supervisor 配置，也不会自动重启。`应用推荐配置` 已停用，因为 `registries_mirror` 不是 HAOS/Supervisor 的受支持全局配置接口。

| 配置键 | 类型 / 默认值 | 说明 |
|---|---|---|
| `auto_switch` | `bool`，默认 `true` | 是否周期执行只读检查；不会自动切换 |
| `probe_interval_hours` | `int`，默认 `6` | 自动检查周期，单位为小时 |
| `enable_ghcr` | `bool`，默认 `true` | 是否检查 `ghcr.io` |
| `enable_dockerio` | `bool`，默认 `true` | 是否检查 `docker.io` |
| `enable_lscr` | `bool`，默认 `true` | 是否检查 `lscr.io` |
| `probe_timeout_seconds` | `int`，默认 `8` | 每个候选源的超时时间 |
| `enable_ota` | `bool`，默认 `false` | 是否显示 OTA 实验功能；默认关闭 |

内置候选源是保守白名单：`ghcr.io` 使用 `ghcr.nju.edu.cn`，`docker.io` 使用 `docker.xuanyuan.me`，`lscr.io` 默认不内置候选。高级设置允许添加合法主机名，但建议先确认该站点支持目标仓库的真实 manifest。

## 使用 / 访问入口

打开 Web 界面后按三步操作：

1. **检查镜像入口**：只读检查真实 manifest，不会修改 `docker.json`，也不会重启 Supervisor。
2. **查看检查结果**：页面只把检查成功的源列为推荐；推荐结果仅供你判断网络是否可达。
3. **清理旧配置**：如果以前使用过旧版本的“应用推荐配置”，并且现在安装加载项一直转圈，点击“清除旧配置并恢复直连”。它只删除旧版写入的 `registries_mirror` 字段，成功后才会请求重启 Supervisor。

自动维护现在只做检查和记录，不会自动切换镜像源。网络短暂抖动不会改变 Supervisor 配置。

需要排障时可在“高级设置”中使用：

- “恢复上次配置”：已停用，不会重新写入旧版镜像映射；
- “清除旧配置并恢复直连”：移除旧版本留下的 `registries_mirror` 字段，回到 Supervisor 原始行为；
- 增删候选镜像源：仅改变候选清单，不会自动应用。

OTA 默认关闭，属于实验功能，不纳入国内关键路径承诺。启用后必须按“检查 → 下载 → 安装 → 重启”逐步操作；板型只使用 Supervisor `/os/info` 返回的 `board`，升级包仍由系统 RAUC 校验官方签名。公益下载代理可能失效，OTA 失败不会影响镜像换源。

## 常见问题

- **为什么安装时没有要求我先直连 GitHub？** 本加载项使用国内预构建镜像入口，首次安装只需要商店仓库和国内入口可达。
- **检查成功但我不想处理，可以不点任何按钮吗？** 可以。检查本身不会写入 Supervisor 配置。
- **所有候选源都失败怎么办？** 当前配置会保持不变。可以稍后重试，或在高级设置中添加你确认可用的候选源；也可以使用“恢复直连”。
- **检查完成，但“应用推荐配置”仍不可点击？** 这表示本次没有任何候选镜像源通过真实 manifest 检查，不是配置已经被写入。页面会显示“暂未找到可用的镜像源”，当前配置保持不变；稍后重试或在高级设置添加已确认可用的候选源。
- **为什么“应用推荐配置”不能点击？** 这是有意停用的安全保护。旧版本写入的字段不是 HAOS/Supervisor 官方接口，可能导致安装加载项一直等待。
- **安装加载项一直转圈怎么办？** 打开本加载项，点击“清除旧配置并恢复直连”，等待 Supervisor 重启完成，再重新安装加载项。
- **为什么 OTA 默认关闭？** OTA 依赖公益下载代理，且涉及宿主系统升级，不属于换源和 HACS 安装的关键路径。
- **这个加载项支持哪些架构？** 只支持 HAOS `amd64` 和 `aarch64`。

## 英文原版

本加载项是自有开发工具，没有独立的英文 README；仓库入口见 [English repository](https://github.com/Treasoni/ha-addon-cn)。
