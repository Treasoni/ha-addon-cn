<!-- zh-guide -->
# Grampsweb

## 简介
Gramps Web 是一款用于创建和分享族谱的 Web 应用，是免费开源系谱软件 Gramps 的 Web 前端。它提供现代化的系谱研究界面、多用户支持与用户管理、丰富的媒体支持（照片、文档等）、高级搜索与过滤、图表与报告生成、多种格式的导入/导出，以及用于集成的 RESTful API。

## 安装
1. 在 Home Assistant → 设置 → 加载项 → 商店，添加本商店仓库：
   - Gitee：https://gitee.com/zhqznc_10603234_123/ha-addon
   - GitHub：https://github.com/Treasoni/ha-addon-cn
2. 搜索 grampsweb 并安装。

## 配置
| 配置键 | 类型 / 默认值 | 说明 |
|--------|---------------|------|
| `CELERY_NUM_WORKERS` | 整数 / `2` | 后台任务 Celery worker 的数量 |
| `GUNICORN_NUM_WORKERS` | 整数 / `8` | Web 请求 Gunicorn worker 的数量 |
| `GRAMPSWEB_SECRET_KEY` | 字符串（可选） / 空 | 会话安全密钥（未设置时自动生成） |
| `GRAMPSWEB_BASE_URL` | 字符串（可选） / 空 | 应用的基础 URL |
| `ssl` | 布尔（可选） / `false` | 启用 SSL/TLS |
| `certfile` | 字符串（可选） / `fullchain.pem` | SSL 证书文件 |
| `keyfile` | 字符串（可选） / `privkey.pem` | SSL 私钥文件 |
| `GRAMPSWEB_EMAIL_HOST` | 字符串（可选） / 空 | SMTP 服务器主机名 |
| `GRAMPSWEB_EMAIL_PORT` | 整数（可选） / 空 | SMTP 服务器端口 |
| `GRAMPSWEB_EMAIL_USE_SSL` | 布尔（可选） / 空 | 使用 SSL 加密（用于 465 端口） |
| `GRAMPSWEB_EMAIL_USE_STARTTLS` | 布尔（可选） / 空 | 使用 STARTTLS 加密（用于 587 端口） |
| `GRAMPSWEB_EMAIL_HOST_USER` | 字符串（可选） / 空 | SMTP 用户名 |
| `GRAMPSWEB_EMAIL_HOST_PASSWORD` | 密码（可选） / 空 | SMTP 密码 |
| `GRAMPSWEB_DEFAULT_FROM_EMAIL` | 字符串（可选） / 空 | 默认发件邮箱 |
| `env_vars` | 列表 / 空 | 额外环境变量（大写或小写命名） |
| `env_vars.name` | 字符串 | 环境变量名，须匹配 `^[A-Za-z0-9_]+$` |
| `env_vars.value` | 字符串（可选） | 环境变量值 |

## 使用 / 访问入口
本加载项未启用 Ingress，通过端口访问：容器端口 `5001/tcp` 映射到宿主端口 `5000`，浏览器访问 http://homeassistant:5000 打开 Web 界面。首次启动后在 Web 界面中创建管理员账户，即可开始建立族谱或导入 GEDCOM 文件。

## 常见问题
1. 数据存储于 `/config` 下的多个目录：数据库在 `/config/config/`，媒体文件在 `/config/media/`，用户账户在 `/config/users/`，临时文件与报告在 `/config/cache/`，搜索索引在 `/config/indexdir/`。建议定期备份整个 `/config` 目录。
2. 性能调整：`CELERY_NUM_WORKERS` 可根据 CPU 核心数调整，`GUNICORN_NUM_WORKERS` 可调大以支持更多并发用户；也可使用外部 MySQL/PostgreSQL 数据库提升性能。
3. 如需邮件通知，请配置 `GRAMPSWEB_EMAIL_*` 相关选项；旧版本中的 `GRAMPSWEB_EMAIL_USE_TLS` 已替换为 `GRAMPSWEB_EMAIL_USE_SSL` 与 `GRAMPSWEB_EMAIL_USE_STARTTLS`。

---
- 英文原版：Home assistant add-on: Grampsweb；链接 https://github.com/alexbelgium/hassio-addons/blob/master/grampsweb/README.md
- 来源仓库：alexbelgium
