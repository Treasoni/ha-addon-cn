<!-- zh-guide -->
# Joplin Server

## 简介
Joplin Server 是一个免费开源的笔记与待办同步服务器，可跨设备同步大量按笔记本组织的笔记。它支持端到端加密、Markdown 编辑、网页剪辑器扩展，以及多种云服务的同步。本加载项基于 etechonomy/joplin-server 的 Docker 镜像构建。

## 安装
1. 在 Home Assistant → 设置 → 加载项 → 商店，添加本商店仓库：
   - Gitee：https://gitee.com/zhqznc_10603234_123/ha-addon
   - GitHub：https://github.com/Treasoni/ha-addon-cn
2. 搜索 joplin 并安装。

## 配置

| 配置键 | 类型 / 默认值 | 说明 |
|--------|--------------|------|
| `APP_BASE_URL` | 字符串 / 默认 `http://your_domain:port` | 服务对外的基础 URL，请改为你的实际访问地址 |
| `data_location` | 字符串 / 默认 `/config/addons_config/joplin` | Joplin 数据存放路径 |
| `DB_CLIENT` | 字符串（可选） | 数据库客户端类型，仅支持 `pg`（PostgreSQL）；MariaDB/MySQL 不支持 |
| `POSTGRES_HOST` | 字符串（可选） | PostgreSQL 服务器主机名 |
| `POSTGRES_PORT` | 整数（可选） | PostgreSQL 服务器端口（默认 5432） |
| `POSTGRES_DATABASE` | 字符串（可选） | PostgreSQL 数据库名 |
| `POSTGRES_USER` | 字符串（可选） | PostgreSQL 用户名 |
| `POSTGRES_PASSWORD` | 字符串（可选） | PostgreSQL 密码 |
| `MAILER_ENABLED` | 整数（可选） | 是否启用邮件服务（1=启用，0=禁用） |
| `MAILER_HOST` | 字符串（可选） | SMTP 服务器主机名 |
| `MAILER_PORT` | 整数（可选） | SMTP 服务器端口 |
| `MAILER_SECURITY` | 枚举（可选） | SMTP 加密方式：`none`、`tls`、`starttls` |
| `MAILER_AUTH_USER` | 字符串（可选） | SMTP 认证用户名 |
| `MAILER_AUTH_PASSWORD` | 字符串（可选） | SMTP 认证密码 |
| `MAILER_NOREPLY_NAME` | 字符串（可选） | 邮件发件人名称 |
| `MAILER_NOREPLY_EMAIL` | 字符串（可选） | 邮件发件人地址 |
| `env_vars` | 列表 / 默认 `[]` | 额外传给容器的环境变量（键名需匹配 `^[A-Za-z0-9_]+$`） |

## 使用 / 访问入口
- 通过浏览器访问宿主端口 22300 打开 Web 界面。
- 首次启动后在界面中创建第一个管理员账户，随后在 Joplin 客户端中配置与服务器的同步。

## 常见问题
- **数据库如何选择？** 默认使用 SQLite；生产环境建议改用 PostgreSQL，且只支持 `pg`（MariaDB/MySQL 不受支持），需安装 PostgreSQL 加载项并配置 `POSTGRES_*` 选项后再重启加载项。
- **邮件功能怎么启用？** 配置 SMTP 服务器相关选项，并将 `MAILER_ENABLED` 设为 1，用于用户注册与通知邮件。
- **升级后启动卡住？** 从 3.5.2 起启动时会自动清理 SQLite 与 PostgreSQL 数据库的陈旧迁移锁，避免阻塞全新安装。
- **支持侧边栏 Ingress 吗？** 目前上游尚未提供 Ingress 支持，需通过端口访问。
- **旧配置项 `MAILER_SECURE`？** 旧版本中的 `MAILER_SECURE` 已由 `MAILER_SECURITY` 取代，请使用新键名。

---
- 英文原版：[Home assistant add-on: Joplin](https://github.com/alexbelgium/hassio-addons/blob/master/joplin/README.md)
- 来源仓库：alexbelgium
