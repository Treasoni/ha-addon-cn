<!-- zh-guide -->
# Nginx Proxy Manager + Static Web Server

## 简介

Nginx Proxy Manager + Static Web Server 将 Nginx Proxy Manager 反向代理管理器和可配置的静态文件服务器结合到一个加载项中。你可以通过 Web 管理界面（端口 81）管理反向代理与 SSL 证书，同时从 Home Assistant 存储（端口 80）提供静态文件服务。相比 Home Assistant 内置的文件夹服务器（只能同时服务单个目录、没有反向代理能力、不支持 SSL/HTTPS、缺少 HTTP 头与缓存控制、不支持 URL 重写与高级路由），本加载项可以从单一界面托管多个站点、管理 SSL 证书并代理流量到其他服务。它封装自 jc21/nginx-proxy-manager 上游镜像。

## 安装

1. 在 Home Assistant → 设置 → 加载项 → 商店，添加本商店仓库：
   - Gitee：https://gitee.com/zhqznc_10603234_123/ha-addon
   - GitHub：https://github.com/Treasoni/ha-addon-cn
2. 搜索 nginx_webserver_proxy 并安装。

## 配置

默认配置即可完成首次运行。可配置选项如下：

| 配置键 | 类型 / 默认值 | 说明 |
| ------ | ------------- | ---- |
| `static_site_enabled` | 布尔，默认 `true` | 是否在端口 80 上启用静态文件服务 |
| `static_site_root` | 字符串，默认 `/share/www` | 静态文件服务的根目录 |
| `static_site_prefix` | 字符串，默认 `/` | 静态站点的 URL 前缀（例如 `/www` 对应 `http://homeassistant.local/www`） |
| `log_level` | 枚举 `list(info\|debug\|warn\|error)`，默认 `info` | 日志详细程度，可选 `info`、`debug`、`warn` 或 `error` |

## 使用 / 访问入口

- **管理界面**：打开 `http://homeassistant.local:81`（端口 `81/tcp` 映射到宿主端口 `81`）访问 NPM 管理后台。
- **静态网站**：将文件放到 `/share/www`（或你配置的 `static_site_root`），通过 `http://homeassistant.local:80/`（端口 `80/tcp` 映射到宿主端口 `80`，支持 NPM 代理主机）访问。
- **HTTPS**：端口 `443/tcp` 映射到宿主端口 `443`，用于 NPM 代理主机的 HTTPS 访问。
- 静态站点与反向代理可以同时在相同端口上运行。

### 默认凭据

首次登录管理界面（端口 81）使用：

- 邮箱：`admin@example.com`
- 密码：`changeme`

首次登录后请立即修改。

## 常见问题

- **路径校验规则是什么？** 启动时会校验路径以确保安全：`/share`、`/media`、`/config` 完全支持（HA 会自动映射）；`/mnt` 允许但不会自动映射，若文件无法访问请在 `/share` 或 `/media` 下创建符号链接；`/`、`/etc`、`/bin`、`/lib`、`/proc`、`/sys` 会被阻止并阻止加载项启动。
- **SSL 证书会丢失吗？** 不会。Let's Encrypt 证书会通过符号链接持久化到 `/data/letsencrypt`，重启后仍然保留。
- **状态数据存放在哪里？** 加载项状态持久化在 `/data` 中，由 Home Assistant Supervisor 管理；如有需要可通过 SSH 直接编辑 NPM 的数据库。
- **如何新增反向代理？** 打开管理界面，添加一个指向其他服务的代理主机，并按需配置 Let's Encrypt SSL。
- **为什么选这个加载项？** 因为它同时提供完整反向代理与真正的静态文件服务器，支持多站点托管、SSL 证书管理与流量代理，弥补了 HA 内置文件夹服务器的不足。

---
- 英文原版：Nginx Proxy Manager + Static Web Server；链接 https://github.com/alexbelgium/hassio-addons/blob/master/nginx_webserver_proxy/README.md
- 来源仓库：alexbelgium
