<!-- zh-guide -->
# Tor

## 简介

Tor 应用通过 Tor 的隐藏服务（Hidden Service）功能，让你的 Home Assistant 实例以 Onion 站点的方式访问。启用该功能后，无需开放防火墙端口或配置 HTTPS 即可实现安全的远程访问。

适用场景：

- 想远程访问 Home Assistant，但不想开放防火墙端口或配置 VPN。
- 不想（或不了解如何）申请 SSL/TLS 证书与配置 HTTPS。
- 希望阻止攻击者扫描/访问你的端口与服务器。
- 希望隐藏家庭 IP 地址，避免第三方窥探你访问 Home Assistant 的流量。

此外，应用还提供指向 Tor 网络的 SOCKS 代理，让任何支持 SOCKS 的应用都能通过你的 Home Assistant 访问 Tor。

## 安装

1. 在 Home Assistant 中进入「设置 → 加载项 → 商店」，点击右上角菜单添加本商店仓库：
   - Gitee：https://gitee.com/zhqznc_10603234_123/ha-addon
   - GitHub：https://github.com/Treasoni/ha-addon-cn
2. 在商店中搜索 `tor`（Tor）并点击安装。
3. 启动应用并在日志中确认一切正常，日志中会显示你的 Onion 地址。

## 配置

> 注意：修改配置后需重启应用才会生效。

| 配置键 | 类型 / 默认值 | 说明 |
| --- | --- | --- |
| `log_level` | 枚举（trace\|debug\|info\|notice\|warning\|error\|fatal），可选 / 空 | 应用的日志输出级别。`trace` 显示全部细节，`debug` 显示详细调试信息，`info` 为正常事件，`warning` 为非错误的异常，`error` 为无需立即处理的错误，`fatal` 为致命错误。推荐使用 `info`。 |
| `socks` | 布尔 / false | 设为 `true` 时在 SOCKS 代理端口监听来自支持 SOCKS 的应用程序的连接，允许局域网内的其他应用使用 Tor 网络。注意：SOCKS 协议未加密且未认证，暴露可能泄露信息或使他人把你的设备当作开放代理。 |
| `http_tunnel` | 布尔 / false | 设为 `true` 时在 HTTP 代理端口监听来自 HTTP 应用的连接，允许局域网内的其他应用通过 HTTP 代理访问 Tor 网络。 |
| `hidden_services` | 布尔 / true | 是否启用 Tor 隐藏服务功能。启用后，无需公开地址即可在防火墙之后提供 Web、SSH 等隐藏服务，且不会向用户暴露你的 IP。 |
| `stealth` | 布尔 / false | 启用 Tor 隐藏服务的「隐身」模式（授权客户端模式），让 Home Assistant 的流量即使对 Tor 网络中的其他节点也保持隐藏。启用后仅授权客户端可访问。 |
| `client_names` | 字符串列表 / 空 | 启用 `stealth` 后必须设置。仅列表中的客户端被授权访问隐藏服务，名称长度为 1–16 个字符，只能使用 `A-Za-z0-9+-_`（不含空格）。客户端需将生成的 `.auth_private` 文件放入其 Tor 的 `ClientOnionAuthDir` 目录。 |
| `ports` | 字符串列表 / ['8123', '8123:80'] | 通过 Tor 隐藏服务发布的主机与端口列表，可填写多个。格式如 `homeassistant:8123:80`（主机:端口:本地端口）或直接写端口号。 |
| `bridges` | 字符串列表 / 空 | Tor 网桥列表，用于绕过审查。访问网桥需通过受支持的传输插件，例如向 Tor 项目申请 OBFS4 网桥地址。 |

## 使用 / 访问入口

本应用不提供 Web 界面。启用隐藏服务后，应用日志中会显示你的 Onion 地址，可在 Tor 浏览器中访问。同时提供两个代理端口：`9050/tcp`（SOCKS 代理端口，映射到宿主端口 9050）和 `9080/tcp`（HTTP 代理端口，映射到宿主端口 9080），供局域网内支持代理的应用使用。

## 常见问题

- **Onion 地址在哪里看**：启动后查看应用日志，其中会列出你的隐藏服务 Onion 地址（`.onion`）。首次启动需要等待片刻生成地址。
- **SOCKS 代理安全提示**：SOCKS 协议未加密且未认证，启用后任何局域网内的人都能使用你的设备作为代理，请谨慎开启。
- **`stealth` 与 `client_names`**：启用 `stealth` 后必须同时配置 `client_names` 授权客户端，否则隐藏服务将不可访问。
- **`ports` 配置格式**：可写端口号，也可写 `主机:端口` 或 `主机:端口:本地端口`，例如 `homeassistant:8123:80`。
- **修改 Onion 地址**：可通过删除应用数据目录下的 Tor 数据来重置 Onion 地址（操作前请先备份）。
- **适用架构**：本应用支持 aarch64、amd64。

---
- 英文原版：Tor；链接 https://github.com/hassio-addons/repository/blob/main/tor/README.md
- 来源仓库：frenck
