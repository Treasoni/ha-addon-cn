<!-- zh-guide -->
# Monica

## 简介
Monica 是一个个人关系管理器（PRM），帮助记录与亲友、同事的关系：对话、活动、重要日期、纪念日与跟进提醒、赠送/收到的礼物、债务与人情、笔记与回忆、日记、礼物灵感等。它内置 Meilisearch 全文搜索，支持多种数据库（SQLite、MariaDB、MySQL）。本加载项基于官方 Monica 应用构建。

## 安装
1. 在 Home Assistant → 设置 → 加载项 → 商店，添加本商店仓库：
   - Gitee：https://gitee.com/zhqznc_10603234_123/ha-addon
   - GitHub：https://github.com/Treasoni/ha-addon-cn
2. 搜索 monica 并安装。

## 配置

| 配置键 | 类型 / 默认值 | 说明 |
|--------|--------------|------|
| `database` | 枚举 / 默认 `sqlite` | 数据库类型：`sqlite`（默认）、`MariaDB_addon`（需安装 MariaDB 加载项）、`Mysql_external`（外部 MySQL/MariaDB） |
| `APP_KEY` | 字符串（可选） | 应用加密密钥，留空自动生成 |
| `DB_DATABASE` | 字符串（可选） | 外部 MySQL/MariaDB 的数据库名 |
| `DB_HOST` | 字符串（可选） | 外部 MySQL/MariaDB 的主机名 |
| `DB_PORT` | 整数（可选） | 外部 MySQL/MariaDB 的端口 |
| `DB_USERNAME` | 字符串（可选） | 外部 MySQL/MariaDB 的用户名 |
| `DB_PASSWORD` | 字符串（可选） | 外部 MySQL/MariaDB 的密码 |
| `meilisearch_key` | 密码（可选） | Meilisearch 主密钥，用于保护内置全文搜索；留空时自动生成并持久化 |
| `MAIL_MAILER` | 字符串（可选） | 邮件驱动：`smtp`、`log`、`sendmail`，默认 `log` |
| `MAIL_HOST` | 字符串（可选） | SMTP 服务器主机名 |
| `MAIL_PORT` | 字符串（可选） | SMTP 服务器端口 |
| `MAIL_USERNAME` | 字符串（可选） | SMTP 用户名 |
| `MAIL_PASSWORD` | 字符串（可选） | SMTP 密码 |
| `MAIL_ENCRYPTION` | 字符串（可选） | SMTP 加密方式：`tls`、`ssl` |
| `MAIL_FROM_ADDRESS` | 字符串（可选） | 发件邮箱地址 |
| `MAIL_FROM_NAME` | 字符串（可选） | 发件人名称 |
| `env_vars` | 列表 / 默认 `[]` | 额外传给容器的环境变量（键名需匹配 `^[A-Za-z0-9_]+$`） |

## 使用 / 访问入口
- 通过浏览器访问宿主端口 8181 打开 Web 界面。
- 首次启动后创建第一个用户账户并完成设置向导，即可开始添加联系人与关系。

## 常见问题
- **如何选择数据库？** `database` 默认 `sqlite`（无需额外配置）；选用 `MariaDB_addon` 时需先安装并运行 MariaDB 加载项；选用 `Mysql_external` 时需填写全部 `DB_*` 选项。
- **Meilisearch 搜索如何保护？** 可通过 `meilisearch_key` 设置主密钥，留空时加载项会自动生成一个持久的密钥，确保内置搜索始终可用。
- **邮件功能怎么用？** 配置 `MAIL_*` 相关选项（如 `MAIL_MAILER: smtp`），即可启用密码重置、邀请与提醒等邮件。

---
- 英文原版：[Home assistant add-on: Monica](https://github.com/alexbelgium/hassio-addons/blob/master/monica/README.md)
- 来源仓库：alexbelgium
