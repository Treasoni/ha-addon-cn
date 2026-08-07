<!-- zh-guide -->
# qBittorrent

## 简介

qBittorrent 是一款跨平台、免费开源的 BitTorrent 下载客户端。本加载项基于 [linuxserver.io](https://www.linuxserver.io/) 的镜像构建，可选支持 OpenVPN 或 WireGuard VPN 隧道、SMB/本地磁盘挂载、备用 Web 界面与 HTTPS，并可通过 Ingress 在 Home Assistant 侧边栏直接访问。

## 安装

1. 在 Home Assistant → 设置 → 加载项 → 商店，添加本商店仓库：
   - Gitee：https://gitee.com/zhqznc_10603234_123/ha-addon
   - GitHub：https://github.com/Treasoni/ha-addon-cn
2. 搜索 `qbittorrent` 并安装。
3. 保存配置并按需调整选项，然后启动加载项，检查日志确认运行正常，最后打开 Web 界面并按需修改软件设置。

## 配置

所有配置项均可在加载项的「配置」页面编辑，保存并重启后生效。

| 配置键 | 类型/默认值 | 说明 |
|--------|-------------|------|
| `PUID` | int / `0` | 文件权限用户 ID |
| `PGID` | int / `0` | 文件权限组 ID |
| `TZ` | str / 空 | 时区（如 `Europe/London`） |
| `Username` | str / `admin` | Web 界面管理员用户名 |
| `SavePath` | str / `/share/qBittorrent` | 默认下载目录 |
| `ssl` | bool / `false` | 为 Web 界面启用 HTTPS |
| `certfile` | str / `fullchain.pem` | SSL 证书文件（位于 `/ssl/`） |
| `keyfile` | str / `privkey.pem` | SSL 私钥文件（位于 `/ssl/`） |
| `whitelist` | str / `localhost,127.0.0.1,172.30.0.0/16,192.168.0.0/16` | 免密码访问的 IP 子网白名单 |
| `customUI` | list / `vuetorrent` | 备用 Web 界面：`default` / `vuetorrent` / `qbit-matUI` / `qb-web` / `custom` |
| `DNS_server` | str / `8.8.8.8,1.1.1.1` | 自定义 DNS 服务器（逗号分隔） |
| `localdisks` | str / 空 | 要挂载的本地磁盘（如 `sda1,sdb1,MYNAS`） |
| `networkdisks` | str / 空 | 要挂载的 SMB 共享（如 `//SERVER/SHARE`） |
| `cifsusername` | str / 空 | SMB 共享用户名 |
| `cifspassword` | str / 空 | SMB 共享密码 |
| `cifsdomain` | str / 空 | SMB 共享域 |
| `openvpn_enabled` | bool / `false` | 启用 OpenVPN 连接 |
| `openvpn_config` | str / 空 | OpenVPN 配置文件文件名（位于 `/addon_configs/db21ed7f_qbittorrent/openvpn/`） |
| `openvpn_username` | str / 空 | OpenVPN 用户名 |
| `openvpn_password` | str / 空 | OpenVPN 密码 |
| `vpn_upnp_enabled` | bool / 空 | 启用 VPN 的 UPnP 端口转发 |
| `wireguard_enabled` | bool / `false` | 启用 WireGuard 隧道 |
| `wireguard_config` | str / 空 | WireGuard 配置文件文件名（仅文件名，如 `ABC.conf`，存放在 `/addon_configs/db21ed7f_qbittorrent/wireguard/`） |
| `qbit_manage` | bool / `false` | 启用 qBit Manage 集成 |
| `run_duration` | str / 空 | 运行时长（如 `12h`、`5d`），用于定时运行模式 |
| `silent` | bool / `false` | 抑制调试信息输出 |
| `env_vars` | list / `[]` | 附加环境变量列表（每项为 `name`/`value`） |
| `log_level` | list / `info` | 日志级别：`trace`/`debug`/`info`/`notice`/`warning`/`error`/`fatal` |

### VPN 配置说明

- **OpenVPN 与 WireGuard 不能同时启用**，需二选一。
- WireGuard 配置文件存放在 `/config/wireguard`（Home Assistant OS 上即 `/addon_configs/<addon_slug>/wireguard/`），`wireguard_config` 只填文件名（如 `ABC.conf`），不要带完整路径。若目录中只有一份 `.conf`，可留空自动选择。仅当你的隧道需要接受入站连接（如站点到站点）时，才需要在加载项选项中暴露 UDP 端口 `51820` 并在路由器上转发；只出不入的商业 VPN 通常无需映射端口。运行时配置同时保留 IPv4 与 IPv6 条目，支持双栈 peer。

### 挂载磁盘

- **本地磁盘**：参见 [Mounting Local Drives in Addons](https://github.com/alexbelgium/hassio-addons/wiki/Mounting-Local-Drives-in-Addons)
- **远程 SMB 共享**：参见 [Mounting Remote Shares in Addons](https://github.com/alexbelgium/hassio-addons/wiki/Mounting-remote-shares-in-Addons)

## 使用 / 访问入口

- **Ingress**：启动后可在 Home Assistant 侧边栏看到 qBittorrent 图标，点击即可进入 Web 界面（无需端口）。
- **直接访问**：`http://homeassistant:8080`（宿主端口映射为 `8081`，即 `http://<HA 主机 IP>:8081`）。
- **默认账号**：用户名 `admin`，密码 `homeassistant`（首次启动的日志中也会显示；登录后建议尽快修改密码）。
- **下载目录**：默认下载目录为 `/share/qBittorrent`；挂载的网络磁盘位于 `/mnt/<共享名>`。
- **端口**：对等（Peer）端口为 `59595/tcp+udp`、备用 `6882/tcp+udp`，Web 界面端口为 `8080/tcp`。为获得最佳下载速度与连通性，建议在路由器上映射对等端口。
- **与 Home Assistant 集成**：可使用官方 [qBittorrent 集成](https://www.home-assistant.io/integrations/qbittorrent/)。

## 常见问题

- **OpenVPN 下的 IPv6 问题**：在 `.ovpn` 配置中加入以下内容，让局域网流量绕过 VPN 并关闭 IPv6：
  ```bash
  route 192.168.1.0 255.255.255.0 net_gateway
  pull-filter ignore "dhcp-option DNS6"
  pull-filter ignore "tun-ipv6"
  pull-filter ignore "ifconfig-ipv6"
  ```
- **CPU 占用 100%**：删除 `/config` 下的 `nova3` 文件夹，然后重启 qBittorrent。
- **WireGuard 连接失败**：确认加载项选项中暴露的 UDP 端口映射到 `51820/udp` 并在路由器上转发（仅入站场景需要）；检查 `/config/wireguard` 中选用的配置文件与 `wireguard_config` 一致；查看加载项日志中 `wg-quick` 输出的具体错误。
- **本地挂载报 `Invalid argument`**：在 `localdisks` 中改用分区标签而不是硬件名（如设备名 `sda1` 改为分区标签）再试。

---
- 英文原版：Home assistant add-on: qbittorrent；链接 https://github.com/alexbelgium/hassio-addons/blob/master/qbittorrent/README.md
- 来源仓库：alexbelgium
