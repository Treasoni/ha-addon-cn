<!-- zh-guide -->
# Zoraxy

## 简介

Zoraxy 是一个通用 HTTP 请求反向代理与转发工具，带简洁的 Web 管理界面。它是 Nginx Proxy Manager 的现代、积极维护的替代品：可以创建反向代理主机、管理 TLS 证书（含 ACME / Let's Encrypt）、设置重定向、访问规则、基础 Web 服务器等。本加载项基于 [tobychui/zoraxy 官方 Docker 镜像](https://github.com/tobychui/zoraxy/tree/main/docker)构建。

## 安装

1. 在 Home Assistant → 设置 → 加载项 → 商店，添加本商店仓库：
   - Gitee：https://gitee.com/zhqznc_10603234_123/ha-addon
   - GitHub：https://github.com/Treasoni/ha-addon-cn
2. 搜索 zoraxy 并安装。
3. 保存配置并启动加载项，然后打开 Web 界面创建管理员账户。

## 配置

所有配置项均可在加载项的「配置」页面编辑，保存并重启后生效。

| 配置键 | 类型 / 默认值 | 说明 |
|--------|--------------|------|
| `NOAUTH` | 布尔 / `false` | 关闭管理界面的登录认证（请谨慎使用） |
| `ZEROTIER` | 布尔 / `false` | 启用 ZeroTier 全球局域网控制器（需要 `NET_ADMIN` 权限与 `/dev/net/tun`，本加载项已授予） |
| `FASTGEOIP` | 布尔 / `false` | 启用高速 GeoIP 查询（约多占 1 GB 内存） |
| `MDNS` | 布尔 / `true` | 启用 mDNS 服务发现 |
| `TZ` | 字符串 / 空 | 时区（如 `Europe/Brussels`） |
| `env_vars` | 对象列表 / `[]` | 附加环境变量列表（每项为 `name`/`value`），可传入上游支持的其他设置（如 `AUTORENEW`、`DB`、`MDNSNAME`） |

## 使用 / 访问入口

- **管理界面**：由于 Zoraxy 作为反向代理需要占用标准 Web 端口，**不走 Home Assistant Ingress**，请直接访问 `http://homeassistant.local:8000`（宿主端口 8000）。
- **反向代理**：监听宿主端口 `80`（HTTP）与 `443`（HTTPS）。请确保这两个端口在宿主机上空闲（未被其他代理加载项占用）；若需从外网访问，请在路由器上转发这些端口。
- **数据持久化**：所有配置、数据库、日志与插件存储在加载项配置目录（`/addon_configs/<slug>_zoraxy/`，容器内为 `/config`），升级与重启后保留。

## 常见问题

- **端口冲突**：`80`/`443` 是反向代理必需的标准端口。若宿主机上已有其他占用它们的服务（如 Nginx Proxy Manager），需先停用。
- **管理员账户**：首次启动后打开管理界面，按提示创建管理员账户，才能进入设置。

---
- 英文原版：Home assistant add-on: Zoraxy；链接 https://github.com/alexbelgium/hassio-addons/blob/master/zoraxy/README.md
- 来源仓库：alexbelgium
