<!-- zh-guide -->
# Let's Encrypt

## 简介
本加载项基于 Certbot，用于从 Let's Encrypt 申请免费的 X.509 证书，为你的网站和 Web 界面启用 TLS 加密。你需要在配置中提供要申请证书的域名以及用于注册的邮箱。申请成功后证书会写入 `/ssl` 共享目录，供 Home Assistant 本体及其他加载项（如 Nginx Proxy Manager、Samba 等）使用。

## 安装
1. 在 Home Assistant → 设置 → 加载项 → 商店，添加本商店仓库：
   - Gitee：https://gitee.com/zhqznc_10603234_123/ha-addon
   - GitHub：https://github.com/Treasoni/ha-addon-cn
2. 搜索 letsencrypt 并安装。

## 配置
该加载项无 Web 界面，所有配置在「配置」页面中填写。核心选项如下：

| 配置键 | 类型/默认值 | 说明 |
| --- | --- | --- |
| `domains` | 字符串列表（必填） | 申请证书的域名列表；使用 `*.yourdomain.com` 可申请泛域名证书 |
| `email` | email（必填） | 注册 Let's Encrypt 账户所用的邮箱地址 |
| `keyfile` | str，默认 `privkey.pem` | 私钥文件输出文件名，写入 `/ssl` 目录 |
| `certfile` | str，默认 `fullchain.pem` | 证书文件输出文件名，写入 `/ssl` 目录 |
| `challenge` | `http` / `dns`，默认 `http` | 域名验证方式 |
| `dns` | 对象 | DNS 验证所需配置（`provider` 及各家服务商的凭证字段，见下文） |
| `key_type` | `ecdsa` / `rsa` | 证书密钥类型；未设置时自动检测已有证书类型，默认 `ecdsa` |
| `elliptic_curve` | `secp256r1` / `secp384r1` | ECDSA 椭圆曲线，需配合 `key_type: ecdsa`；未设置时使用 Certbot 默认值 |
| `acme_server` | url | 自定义 ACME 服务器地址（默认使用 Let's Encrypt 官方服务器） |
| `acme_root_ca_cert` | str | 自定义 ACME 服务器使用的非受信任根 CA 证书内容（按需加入信任库） |
| `dry_run` | bool | certbot 试运行；使用自定义服务器时自动忽略 |
| `test_cert` | bool | 从 Let's Encrypt 预演（staging）服务器申请测试证书；使用自定义服务器时自动忽略 |
| `verbose` | bool | 开启 certbot 详细日志 |
| `force_renew` | bool | 无论是否到期都强制续期 |
| `eab_kid` | str | 外部账户绑定（EAB）的 Key ID |
| `eab_hmac_key` | str | 外部账户绑定（EAB）的 HMAC 密钥 |

### `dns` 块（DNS 验证）
选择 `challenge: dns` 时需设置 `dns.provider`，并填写对应服务商的凭证。

| 配置键 | 类型/默认值 | 说明 |
| --- | --- | --- |
| `dns.provider` | 字符串列表 | DNS 服务商标识，如 `dns-cloudflare`、`dns-route53`、`dns-lego`（通用，支持任意 lego 服务商）等 |
| `dns.propagation_seconds` | int(60–3600) | DNS 生效等待时间（传播等待秒数） |
| `dns.dns_multi_nameservers` | str | 逗号分隔的公共 DNS 服务器列表，用于 split DNS 环境下的区域解析；端口可选，默认 53 |
| `dns.lego_provider` | str | 使用 `dns-lego` 时指定的 lego 服务商名称 |
| `dns.lego_env` | 字符串列表 | 使用 `dns-lego` 时传递给 lego 的 `KEY=VALUE` 环境变量 |

各服务商对应的凭证字段（均为可选字符串，按需填写）：
- **Route 53** (`dns-route53`)：`aws_access_key_id`、`aws_secret_access_key`、`aws_region`（默认 `us-east-1`）
- **Azure** (`dns-azure`，已弃用)：`azure_config`（凭证文件名，放入 `/share`）
- **Bunny** (`dns-bunny`)：`bunny_api_key`
- **Cloudflare** (`dns-cloudflare`)：`cloudflare_api_token`（推荐）或 `cloudflare_api_key` + `cloudflare_email`
- **ClouDNS** (`dns-cloudns`)：`cloudns_auth_id`、`cloudns_auth_password`、`cloudns_sub_auth_id`
- **deSEC** (`dns-desec`)：`desec_token`
- **DigitalOcean** (`dns-digitalocean`)：`digitalocean_token`
- **DirectAdmin** (`dns-directadmin`)：`directadmin_url`、`directadmin_username`、`directadmin_password`
- **DNSimple** (`dns-dnsimple`)：`dnsimple_token`
- **DNS Made Easy** (`dns-dnsmadeeasy`)：`dnsmadeeasy_api_key`、`dnsmadeeasy_secret_key`
- **domainoffensive** (`dns-domainoffensive`)：`domainoffensive_token`
- **DreamHost** (`dns-dreamhost`)：`dreamhost_api_key`
- **DuckDNS** (`dns-duckdns`)：`duckdns_token`
- **Dynu** (`dns-dynu`)：`dynu_auth_token`
- **easyDNS** (`dns-easydns`)：`easydns_endpoint`、`easydns_key`、`easydns_token`
- **EuroDNS** (`dns-eurodns`)：`eurodns_applicationId`、`eurodns_apiKey`
- **Gandi** (`dns-gandi`)：`gandi_token`（推荐）或 `gandi_api_key`
- **gehirn** (`dns-gehirn`)：`gehirn_api_token`、`gehirn_api_secret`
- **GoDaddy** (`dns-godaddy`)：`godaddy_key`、`godaddy_secret`
- **Google Cloud** (`dns-google`)：`google_creds`（凭证文件名，放入 `/share`）
- **Hurricane Electric** (`dns-he`，已弃用)：`he_user`、`he_pass`
- **Hetzner** (`dns-hetzner`)：`hetzner_api_token`
- **HTTP request** (`dns-httpreq`)：`httpreq_endpoint`、`httpreq_username`、`httpreq_password`
- **Infomaniak** (`dns-infomaniak`)：`infomaniak_api_token`
- **INWX** (`dns-inwx`)：`inwx_username`、`inwx_password`、`inwx_shared_secret`
- **IONOS** (`dns-ionos`)：`ionos_prefix`、`ionos_secret`
- **Joker** (`dns-joker`)：`joker_username`、`joker_password`
- **Linode** (`dns-linode`)：`linode_key`
- **Loopia** (`dns-loopia`)：`loopia_user`、`loopia_password`
- **LuaDNS** (`dns-luadns`)：`luadns_email`、`luadns_token`
- **mijn.host** (`dns-mijn-host`)：`mijn_host_api_key`
- **Namecheap** (`dns-namecheap`)：`namecheap_username`、`namecheap_api_key`
- **Netcup** (`dns-netcup`)：`netcup_customer_id`、`netcup_api_key`、`netcup_api_password`
- **Njalla** (`dns-njalla`)：`njalla_token`
- **noris network** (`dns-noris`)：`noris_token`
- **NS1** (`dns-nsone`)：`nsone_api_key`
- **OVH** (`dns-ovh`)：`ovh_endpoint`、`ovh_application_key`、`ovh_application_secret`、`ovh_consumer_key`
- **Plesk** (`dns-plesk`)：`plesk_api_url`、`plesk_username`、`plesk_password`
- **Porkbun** (`dns-porkbun`)：`porkbun_key`、`porkbun_secret`
- **RFC2136** (`dns-rfc2136`)：`rfc2136_server`、`rfc2136_port`、`rfc2136_name`、`rfc2136_secret`、`rfc2136_algorithm`
- **SakuraCloud** (`dns-sakuracloud`)：`sakuracloud_api_token`、`sakuracloud_api_secret`
- **Simply.com** (`dns-simply`)：`simply_account_name`、`simply_api_key`
- **TransIP** (`dns-transip`)：`transip_username`、`transip_api_key`（RSA 私钥内容）
- **WebSupport** (`dns-websupport`)：`websupport_identifier`、`websupport_secret_key`

> 提示：`cloudns_sub_auth_user`、`dreamhost_baseurl`、`gandi_sharing_id`、`ionos_endpoint`、`joker_domain`、`linode_version`、`rfc2136_sign_query`、`transip_global_key` 自 v6.0.0 起已不再支持，请勿再配置。

## 使用 / 访问入口
该加载项**没有 Web 界面或 ingress**，属于"启动后运行一次"的类型：

1. 配置完成后点击「启动」，加载项即向 Let's Encrypt 申请证书；申请完成后自动停止。
2. 证书文件写入 `/ssl` 目录下的 `keyfile` 与 `certfile` 指定文件（默认 `privkey.pem`、`fullchain.pem`）。
3. 其他加载项默认会指向这些证书路径；也可通过 **Samba** 加载项在 `ssl` 共享中查看这些文件。

**验证方式（challenge）二选一：**
- **HTTP 验证**（`challenge: http`）：需要将 80 端口映射到外网（默认映射 `80/tcp`），且域名解析到本机公网 IP；**不支持**泛域名证书。
- **DNS 验证**（`challenge: dns`）：需要在 `dns` 块选择支持的 DNS 服务商并填写凭证；**支持**泛域名证书（`*.yourdomain.com`），且无需在路由器上开放端口。

**配置 Home Assistant 使用证书**（在 `configuration.yaml` 中）：
```yaml
http:
  server_port: 443
  ssl_certificate: /ssl/fullchain.pem
  ssl_key: /ssl/privkey.pem
```

## 常见问题
- **证书不会自动续期**：本加载项只在启动时检查并续期（通常在到期前 30 天）。可通过 Home Assistant 自动化，用「加载项重启」动作每天晚上重启本加载项来实现自动续期。
- **如何强制续期**：将 `force_renew` 设为 `true` 再启动一次；续期完成后记得改回 `false` 或移除该选项，否则每次运行都会强制重新签发证书。
- **UI 编辑模式下配置 DNS**：在「DNS Provider configuration」输入框中，只粘贴 `dns:` 键**下面**的内容（如 `provider: dns-cloudflare`、`cloudflare_email: ...`），不要包含 `dns:` 本身，否则会解析失败。
- **续期报 `failed to find zone`**：通常是 split DNS 环境中本地 DNS 返回的 SOA 与服务商不一致，可设置 `dns.dns_multi_nameservers`（如 `'1.1.1.1,8.8.8.8'`）使用公共 DNS 解析区域。

---
- 英文原版：Home Assistant App: Letsencrypt（[链接](https://github.com/home-assistant/addons/blob/master/letsencrypt/README.md)）
- 来源仓库：official
