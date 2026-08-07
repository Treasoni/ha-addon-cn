<!-- zh-guide -->
# Transmission Openvpn

## 简介

Transmission 是一款 BitTorrent 下载客户端。本加载项在 Transmission 之上通过 OpenVPN 隧道将所有流量加密转发，从而在匿名、安全的 VPN 连接下进行下载。它基于 haugene/docker-transmission-openvpn 镜像构建，提供 Web 界面（WebUI）。

## 安装

1. 在 Home Assistant → 设置 → 加载项 → 商店，添加本商店仓库：
   - Gitee：https://gitee.com/zhqznc_10603234_123/ha-addon
   - GitHub：https://github.com/Treasoni/ha-addon-cn
2. 搜索 transmission_openvpn 并安装。

## 配置

选项说明参见上游 haugene/docker-transmission-openvpn 文档。修改配置后需要重启加载项才能生效。

| 配置键 | 类型/默认值 | 说明 |
| ------ | ----------- | ---- |
| `env_vars` | 列表，默认空 | 传入容器的自定义环境变量列表，每项包含 `name`（变量名，须匹配 `^[A-Za-z0-9_]+$`）与 `value`（变量值，可选）。 |
| `DEBUG` | 布尔，默认 `false` | 是否输出调试日志。 |
| `DNS_server` | 可选字符串，默认 `8.8.8.8,1.1.1.1` | 自定义 DNS 服务器（多个以逗号分隔）。 |
| `LOCAL_NETWORK` | 字符串，默认 `192.168.178.0/24` | 本地网络 CIDR，用于放行局域网内的访问。 |
| `OPENVPN_CONFIG` | 可选字符串，默认空 | 自定义 OpenVPN 配置文件（ovpn 文件名，不含扩展名），需配合 `OPENVPN_PROVIDER` 设为 `custom` 使用。 |
| `OPENVPN_PROVIDER` | 枚举（custom/anonine/mullvad/nordvpn/pia/protonvpn/windscribe 等数十家），默认空 | VPN 提供商名称；设为 `custom` 时可加载自定义 ovpn 文件。 |
| `OPENVPN_USERNAME` | 字符串，默认 `user` | OpenVPN 登录用户名。 |
| `OPENVPN_PASSWORD` | 字符串，默认 `pass` | OpenVPN 登录密码。 |
| `PGID` | 整数，默认 `0` | 文件权限使用的组 ID。 |
| `PUID` | 整数，默认 `0` | 文件权限使用的用户 ID。 |
| `TRANSMISSION_HOME` | 字符串，默认 `/config/addons_config/transmission` | Transmission 的配置目录。 |
| `TRANSMISSION_DOWNLOAD_DIR` | 字符串，默认 `/share/downloads` | 完成下载文件的存放目录。 |
| `TRANSMISSION_INCOMPLETE_DIR` | 字符串，默认 `/share/incomplete` | 未完成下载文件的存放目录。 |
| `TRANSMISSION_WATCH_DIR` | 字符串，默认 `/share/watch_dir` | 监视目录，放入其中的种子文件会被自动添加。 |
| `TRANSMISSION_WEB_UI` | 枚举（standard/combustion/flood-for-transmission/kettu/shift/transmissionic/transmission-web-control），默认 `flood-for-transmission` | Web 界面样式。 |
| `WEBPROXY_ENABLED` | 布尔，默认 `true` | 是否启用内置 Web 代理（默认端口 `8118`）。 |
| `auto_restart` | 可选布尔，默认空 | VPN 隧道断开时是否自动重启加载项。 |
| `cifsdomain` | 可选字符串，默认空 | 网络共享（SMB）的域/工作组。 |
| `cifspassword` | 可选字符串，默认空 | 网络共享（SMB）的密码。 |
| `cifsusername` | 可选字符串，默认空 | 网络共享（SMB）的用户名。 |
| `localdisks` | 可选字符串，默认空 | 需要挂载的本地磁盘，例如 `sda1,sdb1`。 |
| `networkdisks` | 可选字符串，默认空 | 需要挂载的 SMB 网络共享，例如 `//SERVER/SHARE`。 |

## 使用 / 访问入口

- 加载项支持 Ingress，启动后可在 Home Assistant 侧边栏看到 Transmission Openvpn 图标，点击进入 Web 界面。
- Web 界面端口为 `9091/tcp`（映射到宿主端口 `9091`），也可直接访问 `你的主机IP:9091`。
- Web 代理端口为 `8118/tcp`（映射到宿主端口 `8118`，可选，可通过 `WEBPROXY_ENABLED` 关闭）。
- Peer 端口为 `51413/tcp` 与 `51413/udp`（映射到宿主端口 `51413`），如需外网做种请在路由器上转发。

## 常见问题

- **如何使用自定义 ovpn 文件（如 AIRVPN）？** 将 `OPENVPN_PROVIDER` 设为 `custom`，然后安装 Filebrowser 等加载项，把 ovpn 文件放入 `/config/addons_config/transmission/openvpn` 目录，最后在 `OPENVPN_CONFIG` 选项中填写文件名（例如 ovpn 文件名为 `AIRVPN.ovpn` 就填 `AIRVPN`）。
- **安装后 Web 界面打不开？** 可删除 `settings.json` 文件后重启加载项。
- **如何修改 Transmission 的高级设置？** 完整设置在 `/config/addons_config/transmission` 目录中。修改前请先停止加载项，因为 Transmission 在停止时会写回当前值，可能覆盖你的更改。
- **局域网无法访问 Web 界面？** 确认 `LOCAL_NETWORK` 正确填写了本地网段（CIDR 格式）。
- **Web 代理如何使用？** Web 代理默认在端口 `8118` 启用，可在 `WEBPROXY_ENABLED` 中关闭，更多说明见上游 docker-transmission-openvpn 文档。
- 从 v4.3.2 起 `LOCAL_NETWORK` 默认由 `192.168.178.0/16` 改为 `192.168.178.0/24`；自 v5.4.0 版本起新增 `env_vars` 选项。
- Home Assistant 项目已弃用 armv7、armhf 与 i386 架构支持，将在 Home Assistant 2025.12 版本中完全移除。

---
- 英文原版：Home assistant add-on: Transmission Openvpn；链接 https://github.com/alexbelgium/hassio-addons/blob/master/transmission_openvpn/README.md
- 来源仓库：alexbelgium
