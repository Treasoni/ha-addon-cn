<!-- zh-guide -->
# HAOS 国内换源

> 自有 add-on **haos-mirror-switcher** 的中文使用指南。解决国内网络下官方 HAOS 拉不到 ghcr.io 镜像、系统固件 OTA 下载慢的问题。

## 简介

官方 HAOS 在国内直连 ghcr.io 常超时，导致 Add-on 装不上、Core 更新拉不动；系统固件 OTA（`.raucb`）走 GitHub Releases，下载慢且易失败。本加载项提供两层加速：

- **镜像源换源（Supervisor 层）**：自动探测可用国内镜像源，把 `ghcr.io` / `docker.io` / `lscr.io` 写入 Supervisor 的 `registries_mirror` 并重启生效；失效自动切换候选源。
- **OTA 固件升级助手**：经国内 gh-proxy 下载**官方签名**升级包，调用系统 RAUC 安装到备用槽位，确认后重启生效。只做下载加速，不替换系统、不改签名，验签仍由系统内置密钥完成。

原理一句话：HAOS 的 Supervisor 负责拉取全部容器镜像，其配置 `/data/docker.json`（HAOS 宿主路径 `/mnt/data/supervisor/docker.json`）里的 `registries_mirror` 可把镜像请求改道到国内镜像站；系统固件更新则通过 gh-proxy 代理官方下载地址加速。

## 安装

> [!important] 手动换源前置步骤（首次必读）
> 本加载项是自有本地构建（`source: local`），构建时需要从 ghcr.io 拉取基础镜像。若你的 HA 当前完全拉不到 ghcr.io，请先按「HAOS 国内换源」教程手动把 Supervisor 镜像源指到国内镜像一次（例如把 `ghcr.io` 映射到 `ghcr.nju.edu.cn`），确认商店与加载项能正常安装后，再安装本加载项接管后续维护。

1. 在 Home Assistant → 设置 → 加载项 → 右上角商店，添加本商店仓库：
   - Gitee：`https://gitee.com/zhqznc_10603234_123/ha-addon`
   - GitHub：`https://github.com/Treasoni/ha-addon-cn`
2. 搜索 `haos-mirror-switcher` 并安装，然后启动。
3. 从侧边栏点击「HAOS 国内换源」打开 Web 界面。

## 配置

本加载项提供以下配置项（均为可选，默认值即推荐使用值）：

| 配置键 | 类型 | 说明 |
|---|---:|---|
| `auto_switch` | bool | 自动换源开关（默认 `true`）：镜像源失效时自动切换候选源并重启 Supervisor |
| `probe_interval_hours` | int | 周期探测间隔（默认 `6` 小时） |
| `probe_timeout_seconds` | int | 单次探测超时（默认 `8` 秒） |
| `enable_ghcr` | bool | 是否管理 ghcr.io 换源（默认 `true`） |
| `enable_dockerio` | bool | 是否管理 docker.io 换源（默认 `true`） |
| `enable_lscr` | bool | 是否管理 lscr.io 换源（默认 `true`） |
| `enable_ota` | bool | 是否启用 OTA 固件升级助手（默认 `true`） |

内置镜像源候选（按优先序，可在 Web 界面增删）：

| 仓库 | 候选镜像源 |
|---|---|
| ghcr.io | `ghcr.nju.edu.cn`、`ghcr.m.daocloud.io`、`ghcr.1ms.run` |
| docker.io | `docker.nju.edu.cn`、`docker.1ms.run`、`docker.xuanyuan.me`、`docker.m.daocloud.io`、`docker.mirrors.ustc.edu.cn` |
| lscr.io | `docker.1panel.live` |

内置 gh-proxy 下载代理（OTA 用，可在 Web 界面增删）：`ghproxy.net`、`gh.zwy.one`、`raw.ihtw.moe`、`gh.llkk.cc`、`ghfast.top`。

**恢复直连**：若所有镜像源失效，可在 Web 界面点「恢复直连」，移除全部镜像映射，让系统回到直连官方源。

## 使用与访问入口

Web 界面分为「镜像源换源」和「OTA 固件升级」两个区域：

- **镜像源换源**：点「立即探测」查看各镜像源可用性；点「一键应用」写入当前可用源并重启 Supervisor；「恢复上次配置」回滚到之前保存的配置；「恢复直连」移除全部映射；下方表格可逐个开关某仓库、增删候选镜像源。
- **OTA 固件升级**：点「检查更新」查看当前与最新版本；「下载升级包」经国内 gh-proxy 下载官方签名升级包（约 200–260MB）；「安装到备用槽位」调用系统 RAUC 安装；安装完成后点「重启系统生效」（系统会短暂离线，约 1–2 分钟自动恢复）。

> [!note] 说明
> 本加载项以 ingress Web 界面方式访问，无需额外开放端口；「一键应用」「重启 Supervisor」「重启系统」会让相关组件短暂重启，属于正常现象，界面会自动恢复。
> 本加载项仅做下载加速与镜像改道，**不替换系统、不改写官方签名**；OTA 安装前可自行在系统设置中备份。

## 常见问题

- **换源后 HA 启动不了怎么办？** 本加载项写入配置前会做 JSON 语法校验，并保留上次可用配置与系统内备份；若仍异常，打开 Web 界面点「恢复上次配置」或「恢复直连」，或按教程在宿主 shell 直接改 `/mnt/data/supervisor/docker.json`。镜像源失效只影响镜像拉取，不影响系统启动；真正会卡启动的是配置非法 JSON，本加载项已双重防住。
- **系统升级后加速失效？** HAOS 升级可能重置 `docker.json`。本加载项启动时会自愈：检测到映射被重置，自动用上次保存的配置重写并重启。
- **所有镜像源都挂了？** 点「恢复直连」移除全部映射回到官方源；同时可在 Web 界面新增可用的候选镜像源（先按教程的探测方法验证后再加）。
- **为什么 OTA 不用 ota.hasscn.top？** 该源托管的是 HAOS-CN 自签名的定制系统包，官方系统安装会因验签失败；本加载项只下载**官方签名**升级包并经 gh-proxy 加速，验签由系统内置密钥完成，安全可溯源。
- **为什么要申请这些权限？** `docker_api` 用于写 Supervisor 配置、`hassio_api`/`admin` 用于重启 Supervisor 与系统、`host_dbus` 用于调用系统 RAUC 安装升级包，均为功能必需；若你的 HAOS 构建拦截 docker socket，可在配置中关闭相关功能或按社区方案调整 AppArmor。
- **OTA 下载总是失败？** 公益 gh-proxy 源会失效/限流。可在 Web 界面增删下载代理，或稍后再试（内置断点续传）。

## 英文原版

本加载项为自有开发工具（`source: local`），无上游英文 README；代码与版本历史见 [商店仓库](https://github.com/Treasoni/ha-addon-cn)。镜像源与 OTA 加速方案对齐社区教程「HAOS 国内换源」。
