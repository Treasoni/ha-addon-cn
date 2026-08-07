<!-- zh-guide -->
# Seafile

## 简介

Seafile 是一个高性能的文件同步与共享平台，同时内置 Markdown 所见即所得编辑、Wiki、文件标签等知识管理功能，适合个人或团队搭建自托管的网盘与知识库。本加载项基于 franchetti/seafile-arm 镜像构建。

## 安装

1. 在 Home Assistant → 设置 → 加载项 → 商店，添加本商店仓库：
   - Gitee：https://gitee.com/zhqznc_10603234_123/ha-addon
   - GitHub：https://github.com/Treasoni/ha-addon-cn
2. 搜索 `seafile` 并安装。

## 配置

| 配置键 | 类型 / 默认值 | 说明 |
|--------|--------------|------|
| `env_vars` | 列表 / 空 | 额外环境变量列表（每项含 `name` 和 `value`），用于向容器传递自定义环境变量 |
| `CONFIG_LOCATION` | 字符串 / 默认 `/config/addons_config/seafile/config.yaml` | 自定义配置文件位置（可选） |
| `FILE_SERVER_ROOT` | 字符串 / 默认 `http://homeassistant.local:8082` | 文件服务器根 URL，用于生成正确的下载链接 |
| `PGID` | 整数 / 默认 `1000` | 文件权限组 ID |
| `PORT` | 字符串 / 默认 `8082` | 文件服务器端口 |
| `PUID` | 整数 / 默认 `1000` | 文件权限用户 ID |
| `SEAFILE_ADMIN_EMAIL` | 字符串（邮箱）/ 默认 `me@example.com` | 管理员邮箱 |
| `SEAFILE_ADMIN_PASSWORD` | 字符串（密码）/ 默认 `a_very_secret_password` | 管理员密码，首次登录后请立即修改 |
| `SERVER_IP` | 字符串 / 默认 `homeassistant.local` | 服务器 IP 或主机名 |
| `TZ` | 字符串 / 默认 `Europe/Paris` | 时区 |
| `data_location` | 字符串 / 默认 `/share/seafile` | 数据存放位置 |
| `database` | 枚举（sqlite / mariadb_addon）/ 默认 `sqlite` | 数据库类型：`sqlite` 或使用 MariaDB 加载项 |
| `url` | 字符串 / 默认 `seafile.example.com` | 外部访问 Seafile 的地址 |
| `localdisks` | 字符串 / 空 | 要挂载的本地磁盘（如 `sda1,sdb1`） |
| `networkdisks` | 字符串 / 空 | 要挂载的 SMB 共享（如 `//SERVER/SHARE`） |
| `cifsusername` | 字符串 / 空 | SMB 共享用户名 |
| `cifspassword` | 字符串 / 空 | SMB 共享密码 |
| `cifsdomain` | 字符串 / 空 | SMB 共享域名 |

## 使用 / 访问入口

启动后，Seahub 网页界面位于宿主端口 8000，文件服务器位于宿主端口 8082。

## 常见问题

- **默认账号**：默认管理员为 `me@example.com` / `a_very_secret_password`，首次登录后请修改管理员凭据。
- **数据库选择**：默认使用 SQLite，生产环境建议选择 MariaDB（`database` 设为 `mariadb_addon`，并先安装 MariaDB 加载项）。
- **文件服务器 URL**：加载项会把 `SERVICE_URL` 与 `FILE_SERVER_ROOT` 写入 `conf/seahub_settings.py`。请保持 `FILE_SERVER_ROOT` 与你实际可访问的文件服务器地址一致，否则下载链接无法正确解析。
- **挂载磁盘时注意**：如果数据库存放在挂载盘上，请确保 SQLite 数据库也位于同一挂载盘，以免挂载异常导致数据丢失。

---
- 英文原版：[Seafile](https://github.com/alexbelgium/hassio-addons/blob/master/seafile/README.md)
- 来源仓库：alexbelgium
