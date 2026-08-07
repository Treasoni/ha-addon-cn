<!-- zh-guide -->
# Firefly III

## 简介

Firefly III 是一款免费、开源的个人财务管理工具（自托管）。它帮你记录支出与收入，从而花得更少、存得更多。本加载项基于官方 Docker 镜像 [fireflyiii/core](https://hub.docker.com/r/fireflyiii/core)。

## 安装

1. 在 Home Assistant → 设置 → 加载项 → 商店，添加本商店仓库：
   - Gitee：https://gitee.com/zhqznc_10603234_123/homeassistant
   - GitHub：https://github.com/Treasoni/ha-addon-cn
2. 搜索 fireflyiii 并安装。
3. 安装后进入配置页，先修改 `APP_KEY`（见下文），点击保存，再启动加载项。
4. 查看加载项日志确认启动正常，然后打开 WebUI 完成软件设置。

## 配置

**⚠️ 重要**：首次启动前必须修改 `APP_KEY`！它是加密密钥，启动前会校验长度（须为 32 个字符，或包含 `base64` 的 base64 密钥）；启动后无法再更改，否则必须重置数据库。

| 配置键 | 类型 / 默认值 | 说明 |
|--------|----------------|------|
| `env_vars` | 列表 | 附加环境变量（键名大写或小写），用于传入额外配置 |
| `APP_KEY` | 字符串 / `CHANGEME_32_CHARS_EuC5dfn3LAPzeO` | 32 位加密密钥，首次运行前必须修改 |
| `CONFIG_LOCATION` | 字符串 / `/config/addons_config/fireflyiii/config.yaml` | 附加配置文件的位置 |
| `DB_CONNECTION` | 列表 / `sqlite_internal` | 数据库类型：`sqlite_internal` / `mariadb_addon` / `mysql` / `pgsql` |
| `DB_HOST` | 字符串（可选） | 数据库主机（用于外部数据库） |
| `DB_PORT` | 字符串（可选） | 数据库端口（用于外部数据库） |
| `DB_DATABASE` | 字符串（可选） | 数据库名（使用 `mariadb_addon` 时默认 `firefly`） |
| `DB_USERNAME` | 字符串（可选） | 数据库用户名（设置后覆盖 MariaDB 加载项自动发现的服务凭据） |
| `DB_PASSWORD` | 字符串（可选） | 数据库密码（同上） |
| `Updates` | 列表（可选）/ 空 | 自动更新计划：`hourly` / `daily` / `weekly` |
| `silent` | 布尔 / `true` | 静默模式：只显示错误；调试时可设为 `false` 查看完整输出 |

数据库说明：
- `sqlite_internal`（默认）：数据保存在 `/config/addons_config/fireflyiii/` 下的 `database` 与 `upload` 目录，随配置目录持久化。
- `mariadb_addon`：使用 Home Assistant 的 MariaDB 加载项，需先安装并启动该加载项；数据库名、用户名、密码留空时使用 MariaDB 加载项自动发现的服务凭据。请确保 MariaDB 数据纳入备份，卸载 MariaDB 加载项会删除 Firefly III 的数据。
- `mysql` / `pgsql`（外部数据库）：需填写 `DB_HOST`、`DB_PORT`、`DB_DATABASE`、`DB_USERNAME`、`DB_PASSWORD`，且数据库必须已存在。

## 使用 / 访问入口

- Web 界面端口：容器端口 `8080`（默认映射到宿主机端口 `3473`）；另有 `8443` 用于 SSL 界面（默认未映射）。
- 首次访问：浏览器打开 `http://homeassistant:3473`（如在其它电脑上访问，请把 `homeassistant` 换成 Home Assistant 的 IP 地址），按向导创建账户并完成首次设置。
- 常用操作：记账、查看报表等均在 WebUI 中完成；除上述配置项外的其余设置都可在软件界面内调整。

## 常见问题

- **修改 `APP_KEY` 后无法登录或数据错乱？** `APP_KEY` 必须在首次启动前设置好，之后再更改会导致加密数据无法读取，只能重置数据库。
- **选择 `mariadb_addon` 启动失败？** 请确认已安装并启动 Home Assistant 的 MariaDB 加载项，并把 MariaDB 数据纳入备份。
- **如何排查问题？** 把 `silent` 设为 `false`，然后查看完整的启动与运行日志。

---
- 英文原版：[Home assistant add-on: fireflyiii](https://github.com/alexbelgium/hassio-addons/blob/master/fireflyiii/README.md)
- 来源仓库：alexbelgium
