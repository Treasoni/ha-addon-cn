<!-- zh-guide -->
# Dnsmasq

## 简介
本加载项用于在 Home Assistant 上搭建并管理一个 Dnsmasq DNS 服务器。通过它你可以操纵 DNS 请求，例如让你的 Home Assistant 域名在内网解析到内部地址，实现本地解析或 Split DNS。

## 安装
1. 在 Home Assistant → 设置 → 加载项 → 商店，添加本商店仓库：
   - Gitee：https://gitee.com/zhqznc_10603234_123/ha-addon
   - GitHub：https://github.com/Treasoni/ha-addon-cn
2. 搜索 dnsmasq 并安装。

## 配置
| 配置键 | 类型 / 默认值 | 说明 |
| --- | --- | --- |
| `defaults` | 字符串列表 / 默认 `8.8.8.8, 8.8.4.4` | 上游 DNS 服务器，本地无法处理的请求转发到这里；端口用 `#` 分隔，如 `192.168.1.2#1053` |
| `forwards` | 列表 / `[]` | 将指定域名转发到其他（非默认）上游 DNS 服务器的列表 |
| `forwards.domain` | 字符串 | 要转发到其他上游服务器的域名 |
| `forwards.server` | 字符串 | 该域名要转发到的目标 DNS 服务器 |
| `hosts` | 列表 / `[]` | 本地静态解析记录列表，可让内网地址解析到指定 IP，甚至覆盖外部域名（Split DNS） |
| `hosts.host` | 字符串 | 要在本地解析的主机名或域名 |
| `hosts.ip` | 字符串 | Dnsmasq 在应答中返回的 IP 地址 |
| `services` | 列表 / `[]` | 用于提供 SRV 记录的列表 |
| `services.srv` | 字符串 | 要解析的服务记录名 |
| `services.host` | 字符串 | 提供该服务的主机 |
| `services.port` | 字符串 | 该服务的端口号 |
| `services.priority` | 整数 | 该服务的优先级 |
| `services.weight` | 整数 | 该服务的权重 |
| `cnames` | 列表 / `[]` | 用于提供 CNAME 记录的列表 |
| `cnames.name` | 字符串 | 要解析的名称 |
| `cnames.target` | 字符串 | 目标名称；仅对 DHCP 或 `/etc/hosts` 中的名称生效 |
| `txts` | 列表 / `[]` | 用于提供 TXT 记录的列表 |
| `txts.name` | 字符串 | 要解析的名称 |
| `txts.value` | 字符串 | TXT 记录的内容字符串 |
| `ptrs` | 列表 / `[]` | 用于提供 PTR（反向解析）记录的列表 |
| `ptrs.ip` | 字符串 | 要反向解析的 IP 地址，以 `.in-addr.arpa` 结尾的倒序形式，如 `4.3.2.1.in-addr.arpa` |
| `ptrs.name` | 字符串 | 反向解析返回的名称 |
| `log_queries` | 布尔 / `false` | 是否记录所有 DNS 查询日志 |
| `cache_size` | 整数 / `150` | Dnsmasq 缓存大小；设为 `0` 可禁用缓存，过大的缓存可能带来性能问题 |

## 使用 / 访问入口
该加载项没有 Web 界面。启动后作为 DNS 服务器监听容器内 53 端口（TCP 与 UDP），宿主端口映射为 53。将你的设备或路由器的 DNS 指向 Home Assistant 主机即可生效。

## 常见问题
- **缓存性能**：`cache_size` 默认 150，设为 `0` 可关闭缓存；注意过大的缓存可能导致性能问题。
- **默认不记录查询日志**：`log_queries` 默认关闭，开启后才会输出 DNS 查询日志。
- **自定义端口的上游服务器**：`defaults` 中的服务器可使用 `#` 指定端口，例如 `192.168.1.2#1053`。
- **CNAME 目标限制**：`cnames.target` 只对来自 DHCP 或 `/etc/hosts` 的名称生效。

---
- 英文原版：Home Assistant App: Dnsmasq（[链接](https://github.com/home-assistant/addons/blob/master/dnsmasq/README.md)）
- 来源仓库：official
