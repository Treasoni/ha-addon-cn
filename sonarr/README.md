<!-- zh-guide -->
# Sonarr

## 简介

Sonarr 是一款面向 Usenet 和 BitTorrent 用户的 PVR（个人视频录像）工具。它可以同时监控多个 RSS 订阅源，自动抓取你喜爱剧集的新集并完成整理与重命名；当更高质量的资源出现时，还能自动升级已下载文件的画质。本加载项基于 linuxserver/docker-sonarr 镜像构建。

## 安装

1. 在 Home Assistant → 设置 → 加载项 → 商店，添加本商店仓库：
   - Gitee：https://gitee.com/zhqznc_10603234_123/ha-addon
   - GitHub：https://github.com/Treasoni/ha-addon-cn
2. 搜索 sonarr 并安装。

## 配置

以下选项通过加载项配置界面设置（其余设置均在 Sonarr 的 WebUI 中完成）：

| 配置键 | 类型/默认值 | 说明 |
|--------|------|---------|
| `env_vars` | list / `[]` | 要传入的额外环境变量列表，每项含 `name`（需为字母数字或下划线）与 `value` |
| `PGID` | int / `0` | 文件权限组 ID |
| `PUID` | int / `0` | 文件权限用户 ID |
| `TZ` | str / 空 | 时区（如 `Europe/London`） |
| `connection_mode` | list / `ingress_noauth` | 连接模式，可选 `ingress_noauth`、`noingress_auth`、`ingress_auth` |
| `localdisks` | str / 空 | 要挂载的本地磁盘（如 `sda1,sdb1,MYNAS`） |
| `networkdisks` | str / 空 | 要挂载的 SMB 网络共享（如 `//SERVER/SHARE`） |
| `cifsusername` | str / 空 | SMB 网络共享用户名 |
| `cifspassword` | str / 空 | SMB 网络共享密码 |
| `cifsdomain` | str / 空 | SMB 网络共享域名 |

连接模式说明：

- `ingress_noauth`（默认）：启用 ingress，并禁用认证以无缝接入 Home Assistant 侧边栏
- `noingress_auth`：禁用 ingress，启用认证，适用于通过外部 URL 直接访问
- `ingress_auth`：同时启用 ingress 与认证

## 使用 / 访问入口

- **Ingress 入口**：通过 Home Assistant 侧边栏直接访问（入口路径为 `sonarr`）。
- **端口访问**：Web 界面端口为 `8989`，可直接访问 `http://homeassistant:8989`。
- **首次使用**：安装并启动加载项后，查看日志确认启动正常，然后打开 WebUI 按引导完成设置（下载客户端、索引器等）。
- **常用操作**：添加剧集跟踪 RSS 订阅源，Sonarr 会自动抓取、整理并重命名新集；下载文件存放于 `/share/downloads`，剧集存放于 `/share/storage/tv`。

## 常见问题

1. **为什么 `ingress_noauth` 模式下没有登录页？** 该模式默认禁用认证以无缝集成 ingress。此时请勿在路由器上把 `8989` 端口暴露到公网，以免产生安全风险；如需外部访问，请改用 `noingress_auth` 模式。
2. **如何挂载本地磁盘或 NAS 共享？** 在加载项配置中填写 `localdisks`（本地磁盘）或 `networkdisks` 及对应的 CIFS 凭据，具体方法见上游 wiki：https://github.com/alexbelgium/hassio-addons/wiki/Mounting-Local-Drives-in-Addons 与 https://github.com/alexbelgium/hassio-addons/wiki/Mounting-remote-shares-in-Addons 。
3. **绝大多数设置在哪里改？** Sonarr 的绝大部分选项在应用自带的 WebUI 中完成；加载项配置界面仅用于设置上述环境变量、文件权限、时区与连接模式等。

---
- 英文原版：Home assistant add-on: Sonarr
- 来源仓库：alexbelgium
