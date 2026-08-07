<!-- zh-guide -->
# WireGuard

## 简介

WireGuard® 是一款极其简单、快速且现代的 VPN，使用业界领先的加密技术，比 IPsec 更快速、简单、轻量且实用，性能也显著优于 OpenVPN。它被设计为通用 VPN，既能运行在嵌入式设备上，也能运行在超级计算机上。本加载项将 WireGuard 打包进 Home Assistant，并自动为服务器和对端（客户端）生成配置。

## 安装

1. 在 Home Assistant → 设置 → 加载项 → 商店，添加本商店仓库：
   - Gitee：https://gitee.com/zhqznc_10603234_123/ha-addon
   - GitHub：https://github.com/Treasoni/ha-addon-cn
2. 搜索 wireguard 并安装。
3. 把 `server.host` 配置为你的 Home Assistant 外部地址（例如 `myautomatedhome.duckdns.org`），将对端名称改为有意义的名称（如 `myphone`），保存并启动加载项，然后在路由器中把 UDP 端口 51820 转发到 Home Assistant。

## 配置

| 配置键 | 类型 / 默认值 | 说明 |
| --- | --- | --- |
| `server.host` | 字符串，默认 `myautomatedhome.duckdns.org` | 客户端连接所用的主机名（DNS 或 IP，不含端口），主要用于生成客户端配置；本地测试可用 `homeassistant.local`，请勿使用 Nabu Casa 等 URL。 |
| `server.interface` | 字符串（可选） | 服务器接口名称，需匹配 `wg[数字]` 格式（如 `wg0`）。 |
| `server.addresses` | 字符串列表，默认 `172.27.66.1` | 分配给服务器/加载项接口的 IP 地址（IPv4/IPv6，可带 CIDR 掩码）；强烈建议使用与家庭网络不同的独立网段。 |
| `server.dns` | 字符串列表，默认 空 | 用于加载项及生成的客户端配置的 DNS 服务器列表；留空则使用 Hass.io 内置 DNS。若运行 AdGuard，可添加 `172.30.32.1` 让客户端获得广告过滤。 |
| `server.private_key` | 字符串（可选） | 服务器 base64 私钥（由 `wg genkey` 生成），支持 `!secret`；留空则自动生成并保存到 `/ssl/wireguard/private_key`。 |
| `server.public_key` | 字符串（可选） | 服务器 base64 公钥（由 `wg pubkey` 计算），支持 `!secret`；留空则根据私钥自动计算。 |
| `server.fwmark` | 字符串（可选） | 出站数据包的 32 位 fwmark，可用 `0x` 前缀表示十六进制。 |
| `server.table` | 字符串（可选） | 控制添加路由所用的路由表；设为 `off` 则完全禁用路由创建。 |
| `server.pre_up` | 字符串（可选） | WireGuard 启动前执行的命令。 |
| `server.pre_down` | 字符串（可选） | WireGuard 停止前执行的命令。 |
| `server.post_up` | 字符串（可选） | WireGuard 启动后执行的命令；默认把 VPN 进来的流量路由到家庭网络，设为 `off` 可禁用该行为。 |
| `server.post_down` | 字符串（可选） | WireGuard 停止后执行的命令；默认移除 `post_up` 创建的规则，设为 `off` 可禁用。 |
| `server.mtu` | 整数（可选） | 手动指定 MTU；留空则根据端点地址或系统默认路由自动确定。 |
| `peers.name` | 字符串，默认 `hassio` | 对端标识名，用于在 `/ssl/wireguard/<name>` 目录存放生成的客户端配置与二维码；最多 32 字符，只能包含字母、数字和中划线（不能以中划线开头或结尾）。 |
| `peers.addresses` | 字符串列表，默认 `172.27.66.2` | 分配给该对端的 IP 地址（IPv4/IPv6，可带 CIDR 掩码）。 |
| `peers.allowed_ips` | 字符串列表，默认 空 | 仅作用于服务器端：允许来自该对端、并转发给它的 IP 范围；留空则使用 `peers.addresses`。可指定 `0.0.0.0/0`、`::/0`。 |
| `peers.client_allowed_ips` | 字符串列表，默认 空 | 仅作用于客户端配置：客户端允许接收/发送的 IP 范围；留空时生成的客户端配置使用 `0.0.0.0/0`（客户端所有流量走 VPN）。 |
| `peers.private_key` | 字符串（可选） | 对端 base64 私钥（由 `wg genkey` 生成），支持 `!secret`；留空则自动生成并保存到 `/ssl/wireguard/<对端名>/`。 |
| `peers.public_key` | 字符串（可选，推荐） | 对端 base64 公钥（由 `wg pubkey` 计算），支持 `!secret`；留空则根据私钥自动计算。建议手动为每个对端提供公钥（更安全）。 |
| `peers.persistent_keep_alive` | 整数（可选） | 保持 NAT/防火墙映射有效的探测间隔（秒，1–65535）；默认 25 秒，设为 `off` 禁用。 |
| `peers.endpoint` | 字符串（可选） | 对端端点（主机或 IP:端口），用于服务器连接对端；留空会自动更新为最近一次成功认证的数据包来源。 |
| `peers.pre_shared_key` | 字符串（可选） | base64 预共享密钥（由 `wg genpsk` 生成），在公钥加密基础上增加一层对称加密，用于后量子防护。 |
| `peers.fwmark` | 字符串（可选） | 仅作用于客户端：出站数据包的 32 位 fwmark，可用 `0x` 前缀表示十六进制。 |
| `log_level` | 枚举，默认 `info` | 日志级别：`trace`、`debug`、`info`、`warning`、`error`、`fatal`。 |

> 注意：修改配置后需要重启加载项才能生效。

## 使用 / 访问入口

- **VPN 隧道**：使用 UDP 端口 `51820/udp`，请在路由器中把该 UDP 端口转发到你的 Home Assistant 主机。
- **状态 API**：加载项在容器端口 `80/tcp` 提供实验性的 WireGuard 状态 API（宿主端口未固定映射），可在 Home Assistant 内通过加载项主机名 `a0d7b954-wireguard` 访问。
- **客户端配置**：生成的客户端配置与二维码保存在 `/ssl/wireguard/<对端名>/` 目录（如 `qrcode.png`），可用 Samba、Visual Studio Code 或 Configurator 等查看，扫码即可在手机上添加连接。

## 常见问题

1. **修改对端配置后客户端不生效**：对端/客户端配置的变更不会自动同步到已配置的客户端，需要手动修改客户端连接，或删除客户端上的 WireGuard 配置后重新扫描二维码导入。
2. **日志出现 "Missing WireGuard kernel module. Falling back to slow userspace implementation."**：HassOS 默认自带 WireGuard 内核支持；若在通用 Linux 上安装，宿主缺少内核模块时加载项会回退到用户态实现（性能下降）。在宿主系统安装 WireGuard 后重启加载项即可恢复最佳性能。
3. **日志出现 "IP forwarding is disabled on the host system!"**：宿主未开启 IP 转发，VPN 客户端流量无法被路由到家庭网络或互联网，需要在宿主系统启用 IP 转发（`sysctl` 设置 `net.ipv4.ip_forward=1`）。
4. **配合 AdGuard 使用**：如运行 AdGuard 加载项，可在 `server.dns` 中添加 `172.30.32.1`，让 VPN 客户端（如手机）在不在家时也享受广告过滤。
5. **`server.host` 使用 Cloudflare 等代理服务**：WireGuard 会尝试连接该代理而非你的家庭网络；建议在 `server.host` 中使用公网 IP，或使用 DuckDNS 等直接指向你 IP 的 DNS 记录。
6. **部分备份不含客户端密钥**：加载项的部分备份不包含 `/ssl/wireguard` 下生成的客户端配置与密钥，请同时备份 `ssl` 目录，以免密钥丢失。

---
- 英文原版：[Home Assistant Community Add-on: WireGuard](https://github.com/hassio-addons/repository/blob/main/wireguard/README.md)
- 来源仓库：frenck
