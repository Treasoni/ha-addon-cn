<!-- zh-guide -->
# Tailscale

## 简介
Tailscale 是一款零配置 VPN，可在几分钟内安装到任意设备（包括你的 Home Assistant 实例），用于搭建安全的网络。它可以跨越防火墙与子网，在你的服务器、电脑与云端实例之间建立私有安全网络，并自动管理防火墙规则，让你在任何地方都能访问自己的设备。

## 安装
1. 在 Home Assistant → 设置 → 加载项 → 商店，添加本商店仓库：
   - Gitee：https://gitee.com/zhqznc_10603234_123/homeassistant
   - GitHub：https://github.com/Treasoni/ha-addon-cn
2. 搜索 tailscale 并安装。

## 配置
在加载项“配置”标签页中可设置以下选项（配置键 | 类型 / 默认值 | 说明）：

| 配置键 | 类型 / 默认值 | 说明 |
| --- | --- | --- |
| `accept_dns` | 布尔 / `true` | 接受管理后台 DNS 页面配置的 tailnet DNS 设置；关闭后 Tailscale 的 DNS 仅解析 tailnet 地址 |
| `accept_routes` | 布尔 / `true` | 接受 tailnet 中其他节点广播的子网路由 |
| `advertise_exit_node` | 布尔 / `true` | 将本实例广播为出口节点（Exit Node），可用其像消费级 VPN 一样路由公网流量 |
| `advertise_connector` | 布尔 / `true` | 将本实例广播为应用连接器（App Connector），按域名强制应用流量经 tailnet 转发 |
| `advertise_routes` | 子网列表 / `["local_subnets"]` | 向 tailnet 广播本设备可达的子网路由（支持 IPv4/IPv6 网段，如 `192.168.1.0/24`）；填 `[]` 可禁用 |
| `always_use_derp` | 布尔 / `false` | 强制所有对等通信走 DERP（禁用 UDP）。一般无需开启，仅在连接经常卡死且重启 APP 才能恢复时尝试 |
| `exit_node` | 字符串 / 未设置 | 指定本设备使用的另一台出口节点（IP 或 tailnet 名称）。默认未启用，需在配置界面点“显示未使用的可选配置项”；与 `advertise_exit_node` 互斥 |
| `log_level` | 枚举 / `info` | 日志级别：`trace`/`debug`/`info`/`notice`/`warning`/`error`/`fatal`。排障时才调低，设为 `info` 或更轻时客户端不会上传日志到 log.tailscale.io |
| `login_server` | URL / `https://controlplane.tailscale.com` | 自定义控制服务器，自建 Headscale 实例时使用 |
| `share_homeassistant` | 枚举 / `disabled` | 取值 `disabled`/`serve`/`funnel`。启用 Tailscale Serve 或 Funnel，为 Home Assistant 提供合法 HTTPS 证书（tailnet 内或公网访问） |
| `share_on_port` | 数字 / `443` | Serve/Funnel 对外服务的端口，仅允许 443、8443、10000 |
| `snat_subnet_routes` | 布尔 / `true` | 让子网设备看到流量源自子网路由器，简化路由配置；做站点间组网（Site-to-site）时可关闭 |
| `stateful_filtering` | 布尔 / `false` | 在转发节点（出口节点、子网路由、应用连接器）上启用有状态包过滤，仅放行既有出站连接的返回包 |
| `tags` | 标签列表 / `[]` | 为本实例指定 ACL 标签，须以 `tag:` 开头，如 `tag:homeassistant` |
| `taildrive` | 对象（各子项布尔）/ `false` | 用 Taildrive 共享的 Home Assistant 目录，子项：`addons`/`addon_configs`/`backup`/`config`/`media`/`share`/`ssl` |
| `taildrop` | 布尔 / `true` | 启用 Taildrop 文件传输，可从其他 Tailscale 设备向本实例发文件；收到的文件存放在 `/share/taildrop` |
| `userspace_networking` | 布尔 / `true` | 用户态网络模式，让本实例（及可选本地子网）可在 tailnet 内访问；如需从 HA 访问 tailnet 其他客户端，可关闭此选项（会在主机创建 `tailscale0` 网卡） |

> 注意：部分选项在 Web UI 中是只读的，只能在配置文件中修改，因为 Web UI 里的改动会在重启加载项后丢失。

## 使用 / 访问入口
- 本加载项提供 Web UI（ingress）入口，安装启动后可在“信息”页打开。
- 使用前需要注册 Tailscale 账号（个人与爱好用途免费，单账号最多 100 台设备）：https://login.tailscale.com/start
- 首次使用：启动加载项 → 查看日志确认正常 → 打开 Web UI 完成登录授权，把 Home Assistant 实例绑定到你的 Tailscale 账号。注意部分浏览器不兼容该授权步骤，建议在桌面或笔记本上使用 Chrome 完成。
- 登录后可在 Tailscale 管理后台 https://login.tailscale.com/ 配置网络：在 Machines 页面找到你的 Home Assistant 实例，可在 “Edit route settings” 中启用 Exit node 与子网路由，并建议选择 “Disable key expiry” 关闭密钥过期，避免设备断连。
- 网络端口：`41641/udp` 用于 WireGuard 与对等（P2P）流量；若某些设备（通常在 CGNAT 网络后）无法建立 P2P 连接，可对该端口做路由器端口转发，并用 `tailscale ping <主机名或IP>` 测试。未设置时默认使用自动选择的端口。

## 常见问题
- **登录授权时浏览器没反应 / 报错？** 部分浏览器与授权步骤不兼容，请改用桌面或笔记本电脑上的 Chrome 浏览器重试；若仍出现奇怪行为，可清除该站点相关 Cookie 和浏览器缓存后重启浏览器。
- **Home Assistant 设备突然连不上 tailnet？** 建议在管理后台 Machines 页面为你的实例选择 “Disable key expiry” 关闭密钥过期，否则密钥到期后连接会丢失。
- **Funnel 域名迟迟无法访问？** 初次配置后，域名最长可能需要约 10 分钟才会对外生效；访问时不要在 URL 中带端口号，Serve/Funnel 默认使用 HTTPS 443 端口。

---
- 英文原版：Home Assistant Community App: Tailscale（https://github.com/hassio-addons/repository/blob/master/tailscale/README.md）
- 来源仓库：frenck
