<!-- zh-guide -->
# AdGuard Home

## 简介

AdGuard Home 是一款全网络范围的广告与跟踪器拦截 DNS 服务器，并支持家长控制（成人内容拦截）功能。它无需在客户端安装任何程序，即可统一管理整个网络中所有设备的 DNS 流量，并提供一个美观易用、功能丰富的 Web 界面来配置过滤规则与各项设置。

## 安装

1. 在 Home Assistant → 设置 → 加载项 → 商店，添加本商店仓库：
   - Gitee：https://gitee.com/zhqznc_10603234_123/homeassistant
   - GitHub：https://github.com/Treasoni/ha-addon-cn
2. 搜索 adguard 并安装。

> 建议：请确保你的 Home Assistant 设备配置了**静态 IP 和静态外部 DNS 服务器**（Settings → System → Network → 配置网络接口 → IPv4 → Static）。仅在路由器上设置固定 IP 并不算真正的静态 IP，跳过此步可能在使用中遇到问题。

## 配置

在加载项“配置”页修改配置后，需要重启加载项才能生效。可选配置键如下：

| 配置键 | 类型/默认值 | 说明 |
| ------ | ----------- | ---- |
| `log_level` | 可选 `list(trace\|debug\|info\|notice\|warning\|error\|fatal)`，默认 `info` | 日志输出详细程度：`trace` 输出全部细节；`debug` 输出调试信息；`info` 常规事件；`warning` 非错误的异常事件；`error` 运行时错误；`fatal` 致命错误。更高级别会自动包含更低级别的日志，默认 `info` 是推荐设置 |
| `ssl` | `bool`，默认 `true` | 是否启用 SSL（HTTPS）。仅对直接访问生效，对 Ingress 入口无效 |
| `certfile` | `str`，默认 `fullchain.pem` | 用于 SSL 的证书文件，必须存放在 `/ssl/` 目录下 |
| `keyfile` | `str`，默认 `privkey.pem` | 用于 SSL 的私钥文件，必须存放在 `/ssl/` 目录下 |
| `leave_front_door_open` | 可选 `bool`，默认关闭 | 设为 `true` 将禁用 AdGuard Home 的登录认证。**强烈不建议启用**，即使加载项仅暴露在内网，风险自负 |

## 使用 / 访问入口

- **Web 界面**：加载项支持 Ingress，安装并启动后点击侧边栏或加载项中的“打开 Web 界面”即可访问，登录使用你的 Home Assistant 账号。
- **DNS 端口**：`53/udp` 映射到宿主机端口 `53`，作为局域网内的 DNS 服务器使用。
- **直接访问（可选）**：Web 界面默认使用端口 `80/tcp`，仅当不使用 Ingress 时才需要它。
- **首次使用**：安装后启动加载项，查看日志确认运行正常，然后打开 Web 界面并用 Home Assistant 账号登录，即可开始配置过滤规则。
- **高级用法（加密 DNS）**：可在 AdGuard Home 内配置本地 DNS-over-HTTPS 与 DNS-over-TLS，配置后需重启加载项。使用 DNS-over-HTTPS 时请同时为加载项和 AdGuard Home 启用 SSL，且两者不能使用同一个 SSL 端口。

## 常见问题

- **为什么建议先配置静态 IP 和静态外部 DNS？** 因为加载项本身就是 DNS 服务器，若设备 IP 或上游 DNS 变动，可能导致整个网络解析异常。
- **SSL 配置不生效？** SSL 设置只作用于直接访问（端口 80），通过 Ingress 访问时不受影响，无需额外配置。
- **不想每次登录可以吗？** 可将 `leave_front_door_open` 设为 `true` 关闭认证，但会带来安全风险，官方强烈不建议。

---
- 英文原版：Home Assistant Community App: AdGuard Home
- 来源仓库：frenck
