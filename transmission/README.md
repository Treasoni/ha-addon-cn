<!-- zh-guide -->
# Transmission

## 简介

Transmission 是一款 BitTorrent 下载客户端，本加载项基于 linuxserver.io 的 docker-transmission 镜像构建，提供简洁易用的 Web 界面，支持种子文件管理与下载任务控制。

## 安装

1. 在 Home Assistant → 设置 → 加载项 → 商店，添加本商店仓库：
   - Gitee：https://gitee.com/zhqznc_10603234_123/ha-addon
   - GitHub：https://github.com/Treasoni/ha-addon-cn
2. 搜索 transmission 并安装。

## 配置

除下列选项外，其余设置可通过应用自身的 Web 界面完成。修改配置后需要重启加载项才能生效。

| 配置键 | 类型/默认值 | 说明 |
| ------ | ----------- | ---- |
| `env_vars` | 列表，默认空 | 传入容器的自定义环境变量列表，每项包含 `name`（变量名，须匹配 `^[A-Za-z0-9_]+$`）与 `value`（变量值，可选）。 |
| `DNS_server` | 可选字符串，默认 `8.8.8.8,1.1.1.1` | 自定义 DNS 服务器（多个以逗号分隔），可避免对本地 DNS 过滤工具（如 AdGuard）造成负载。 |
| `PGID` | 整数，默认 `0` | 文件权限使用的组 ID。 |
| `PUID` | 整数，默认 `0` | 文件权限使用的用户 ID。 |
| `TZ` | 可选字符串，默认空 | 时区，例如 `Europe/London`。 |
| `cifsdomain` | 可选字符串，默认空 | 网络共享（SMB）的域/工作组。 |
| `cifspassword` | 可选字符串，默认空 | 网络共享（SMB）的密码。 |
| `cifsusername` | 可选字符串，默认空 | 网络共享（SMB）的用户名。 |
| `customUI` | 枚举（standard/transmission-web-control/kettu/flood-for-transmission），默认 `flood-for-transmission` | Web 界面样式：`standard` 为默认界面，其余为第三方 UI（其中 `flood-for-transmission` 为默认选择的界面）。 |
| `download_dir` | 字符串，默认 `/share/downloads` | 完成下载文件的存放目录。 |
| `incomplete_dir` | 可选字符串，默认 `/share/incomplete` | 未完成下载文件的存放目录。 |
| `localdisks` | 可选字符串，默认空 | 需要挂载的本地磁盘，例如 `sda1,sdb1,MYNAS`。 |
| `networkdisks` | 可选字符串，默认空 | 需要挂载的 SMB 网络共享，例如 `//SERVER/SHARE`。 |
| `pass` | 可选字符串，默认空 | Web 界面的登录密码。 |
| `smbv1` | 可选布尔，默认空 | 是否启用 SMB v1 协议。 |
| `user` | 可选字符串，默认空 | Web 界面的登录用户名。 |
| `watch_dir` | 可选字符串，默认空 | 监视目录，放入其中的种子文件会被自动添加。 |
| `whitelist` | 可选字符串，默认空 | 允许访问 Web 界面的 IP 白名单。 |

## 使用 / 访问入口

- 加载项支持 Ingress，启动后可在 Home Assistant 侧边栏看到 Transmission 图标，点击进入 Web 界面。
- Web 界面端口为 `9091/tcp`（映射到宿主端口 `9091`），也可以直接访问 `homeassistant:9091`。
- Peer 端口为 `51413/tcp` 与 `51413/udp`（映射到宿主端口 `51413`），如需外网做种请在路由器上转发该端口。

## 常见问题

- **设置文件被重置？** 若日志中出现 `settings.json` 被重置（参见上游 issue #1269），可安装 Filebrowser 加载项，删除 `/homeassistant/addons_config/transmission` 与 `/homeassistant/addons_config/transmission-ls` 目录后重试。
- **如何修改高级设置？** Transmission 的完整设置在 `/share/transmission/settings.json` 中。修改前请先停止加载项，因为 Transmission 在关闭时会覆盖写入该文件。
- **如何挂载本地磁盘或远程共享？** 分别通过 `localdisks` 与 `networkdisks` 配置，详细步骤参见上游 wiki「Mounting Local Drives in Addons」与「Mounting Remote Shares in Addons」。
- 自 4.0.5-2 版本起默认启用 flood 作为 Web UI（此前默认界面存在已知问题）。
- Home Assistant 项目已弃用 armv7、armhf 与 i386 架构支持，将在 Home Assistant 2025.12 版本中完全移除。

---
- 英文原版：Home assistant add-on: Transmission；链接 https://github.com/alexbelgium/hassio-addons/blob/master/transmission/README.md
- 来源仓库：alexbelgium
