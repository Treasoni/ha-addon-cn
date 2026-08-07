<!-- zh-guide -->
# Inadyn

## 简介
Inadyn（In-a-Dyn）是一个小巧简单的动态 DNS（DDNS）客户端，支持 HTTPS，可自动将你的域名与公网 IP 保持同步，常见于路由器与上网网关中，也适用于带冗余（备份）连接的环境。它支持大量 DDNS 提供商，未内置支持的提供商可通过自定义 provider 配置。本加载项没有 Web 界面，所有配置均在加载项选项中完成。

## 安装
1. 在 Home Assistant → 设置 → 加载项 → 商店，添加本商店仓库：
   - Gitee：https://gitee.com/zhqznc_10603234_123/ha-addon
   - GitHub：https://github.com/Treasoni/ha-addon-cn
2. 搜索 inadyn 并安装。

## 配置

| 配置键 | 类型 / 默认值 | 说明 |
|--------|--------------|------|
| `verify_address` | 布尔（可选） | 是否通过检查 IP 的服务验证公网 IP 地址 |
| `fake_address` | 布尔（可选） | 是否使用模拟地址用于测试 |
| `allow_ipv6` | 布尔（可选） | 是否启用 IPv6 支持 |
| `iface` | 字符串（可选） | 要使用的网络接口，如 `eth0` |
| `iterations` | 整数（可选） | 迭代次数（0 表示无限） |
| `period` | 整数（可选） | 更新周期（秒），默认 300 秒 |
| `forced_update` | 整数（可选） | 强制更新间隔（秒） |
| `secure_ssl` | 布尔（可选） | 是否启用严格的 SSL 校验 |
| `providers` | 列表（对象） | DDNS 提供商配置列表，每个条目需 `provider`、`username`、`password`、`hostname`，可选字段见下方说明 |
| `env_vars` | 列表 / 默认 `[]` | 额外传给容器的环境变量（键名需匹配 `^[A-Za-z0-9_]+$`） |

### DDNS 提供商配置（providers）

每个 provider 条目支持以下字段：`provider`（提供商名称或自定义标识）、`custom_provider`（是否为自定义提供商）、`username`（用户名或令牌）、`password`（密码或 API 密钥）、`hostname`（要更新的域名）、`ssl`（更新时是否使用 SSL）、`ddns_server`/`ddns_path`（自定义 DDNS 服务器与更新路径）、`checkip_server`/`checkip_path`/`checkip_ssl`（自定义 IP 检查）、`append_myip`（是否在请求中附带 IP）、`ttl`、`wildcard`、`proxied`、`user_agent`。

简单的 DuckDNS 示例：
```json
{
  "providers": [
    { "provider": "duckdns", "username": "your-token", "hostname": "sub.duckdns.org" }
  ]
}
```

自定义提供商示例（`custom_provider` 设为 `true`，`ddns_path` 中的令牌含义见 inadyn.conf(5) 手册页）：
```json
{
  "providers": [
    {
      "provider": "arbitraryname",
      "username": "username",
      "password": "password",
      "hostname": "your.domain.com",
      "ddns_server": "api.cp.easydns.com",
      "ddns_path": "/somescript.php?hostname=%h&myip=%i",
      "custom_provider": true
    }
  ]
}
```

## 使用 / 访问入口
- 本加载项没有 Web 界面，配置完成后启动即可在后台持续更新 DDNS。

## 常见问题
- **同一提供商下多个子域名怎么配置？** 需要为每个子域名分别列举 provider，并用 `domains.google.com:1`、`domains.google.com:2`、`domains.google.com:3` 这样的形式区分。
- **不支持的提供商怎么办？** 可将 `custom_provider` 设为 `true`，并用 `ddns_server`、`ddns_path` 等字段按 inadyn 的规则自定义更新请求。
- **配置项很多，需要都填吗？** 不需要，只填写必要的即可，一个典型的 DuckDNS 配置只需要 `provider`、`username` 与 `hostname`。

---
- 英文原版：[Home assistant add-on: Inadyn](https://github.com/alexbelgium/hassio-addons/blob/master/inadyn/README.md)
- 来源仓库：alexbelgium
