<!-- zh-guide -->
# Duck DNS

## 简介
Duck DNS 是一个免费的动态 DNS（DynDNS / DDNS）服务，可将 duckdns.org 的子域名解析到你指定的 IP 地址。本加载项会自动更新你的 Duck DNS IP，并内置 Let's Encrypt 支持，自动签发并续期 SSL 证书。

## 安装
1. 在 Home Assistant → 设置 → 加载项 → 商店，添加本商店仓库：
   - Gitee：https://gitee.com/zhqznc_10603234_123/homeassistant
   - GitHub：https://github.com/Treasoni/ha-addon-cn
2. 搜索 duckdns 并安装。

## 配置

| 配置键 | 类型 / 默认值 | 说明 |
| ------ | ------------- | ---- |
| `token` | 字符串（必填） | DuckDNS 账户页顶部的认证令牌，用于修改你账户下注册的子域名。 |
| `domains` | 字符串列表（必填） | 你账户下注册的 DuckDNS 子域名，命名格式如 `my-domain.duckdns.org`。支持通配符语法 `*.my-domain.duckdns.org > my-domain.duckdns.org` 签发通配符证书。 |
| `aliases` | 对象列表（可选） | DNS 别名，用于把自定义域名指向 DuckDNS 子域名。每个条目为 `alias`（你的域名）与 `domain`（DuckDNS 子域名），配合 CNAME 记录使用。不要把自定义域名放进 `domains`。 |
| `lets_encrypt.accept_terms` | 布尔值 / `false` | 阅读并接受 Let's Encrypt 订阅协议后设为 `true` 才能使用其服务。 |
| `lets_encrypt.algo` | 枚举 / `secp384r1` | 证书公钥算法，支持 `rsa`、`prime256v1`、`secp384r1`。 |
| `lets_encrypt.certfile` | 字符串 / `fullchain.pem` | 生成的证书文件名，存放在 `/ssl/`，建议保持默认以便兼容。 |
| `lets_encrypt.keyfile` | 字符串 / `privkey.pem` | 生成的私钥文件名，存放在 `/ssl/`，建议保持默认以便兼容。 |
| `seconds` | 整数 / `300` | 更新 DuckDNS 子域名和续期 Let's Encrypt 证书的间隔秒数。 |
| `ipv4` | 字符串（可选） | 手动指定 IPv4 地址，覆盖自动检测；也可填 URL，将抓取其内容作为地址（如 `https://api.ipify.org/`）。 |
| `ipv6` | 字符串（可选） | 手动指定 IPv6 地址，覆盖自动检测；也可填 URL，将抓取其内容作为地址（如 `https://api6.ipify.org/`）。 |

### 让 Home Assistant 使用证书
本加载项将证书写入 `/ssl/`，还需在 Home Assistant 的 `configuration.yaml` 中配置 HTTP 集成以启用 HTTPS：

```yaml
http:
  ssl_certificate: /ssl/fullchain.pem
  ssl_key: /ssl/privkey.pem
```

## 使用 / 访问入口
本加载项为后台服务，没有界面或端口访问入口，配置完成后自动运行。使用步骤：

1. 访问 [DuckDNS.org](https://www.duckdns.org/)，通过 Google、Github、Twitter 或 Reddit 账号登录并注册免费账户。
2. 在 `Domains` 区输入想注册的子域名并点击 `add domain`，成功后页面会显示当前公网 IP。
3. 在加载项配置中填入 DuckDNS 令牌（`token`）和已注册的完整域名（`domains`）。
4. 若使用自定义域名，请在 DNS 服务商处配置 CNAME 指向你的 DuckDNS 子域名，并建议将 TTL 设为较低值（通常低于 60）；证书签发走 dns-01 验证，可能还需配置 `_acme-challenge` 的 CNAME。

## 常见问题
- **登录方式**：DuckDNS 需要免费账户，仅支持通过 Google、Github、Twitter 或 Persona 等第三方服务登录。
- **子域名数量限制**：免费 DuckDNS 账户最多注册五个子域名。
- **IPv6 自动检测不生效**：DuckDNS 自带的 IPv6 自动检测目前实际不可用，可通过在 `ipv6` 选项中填写 URL（如 `https://api6.ipify.org/`）来获取真实地址。

---
- 英文原版：Home Assistant App: DuckDNS；链接 https://github.com/home-assistant/addons/blob/master/duckdns/README.md
- 来源仓库：official
