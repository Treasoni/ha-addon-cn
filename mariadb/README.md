<!-- zh-guide -->
# MariaDB

## 简介

MariaDB 是一个开源（GPLv2 协议）的关系型 SQL 数据库服务器，可以作为 Home Assistant 的数据库后端，用于存储历史记录等数据。

## 安装

1. 在 Home Assistant → 设置 → 加载项 → 商店，添加本商店仓库：
   - Gitee：https://gitee.com/zhqznc_10603234_123/ha-addon
   - GitHub：https://github.com/Treasoni/ha-addon-cn
2. 搜索 mariadb 并安装。

## 配置

安装完成后，在加载项"配置"页中可设置以下选项：

| 配置键 | 类型 / 默认值 | 说明 |
| --- | --- | --- |
| `databases`（必填） | list[str]，默认 `homeassistant` | 要创建的数据库名称，可配置多个，例如 `homeassistant`。 |
| `logins`（必填） | list[object]，默认 `username: homeassistant`、`password: null` | 创建数据库用户（对应 MariaDB 的 CREATE USER）。 |
| `logins.username`（必填） | str | 数据库登录用户名，例如 `homeassistant`。 |
| `logins.password`（必填） | password | 用户的登录密码，应设置得足够强且唯一。 |
| `rights`（必填） | list[object]，默认 `username: homeassistant`、`database: homeassistant` | 为用户授予数据库权限（对应 MariaDB 的 GRANT）。 |
| `rights.username`（必填） | str | 应等于 `logins.username` 中定义的用户名。 |
| `rights.database`（必填） | str | 应等于 `databases` 中定义的数据库名。 |
| `rights.privileges`（可选） | list[str]，如 `SELECT`、`CREATE` | 授予该用户的权限列表；省略时为该用户授予全部权限（ALL PRIVILEGES）。 |
| `mariadb_server_args`（可选） | list[str] | 追加 MariaDB 服务器启动参数，例如 `--innodb_buffer_pool_size=512M`，可用于大型数据库迁移时缓解内存不足问题。 |

> 提示：默认仅创建一个 `homeassistant` 用户并授予全部权限。若要让其他应用只读访问数据库，可另建一个仅授予 `SELECT` 等只读权限的用户。

## 使用 / 访问入口

本加载项没有 Web 界面（无 ingress），通过 MySQL 协议（端口 3306）对外提供服务，默认情况下 3306 端口处于关闭状态。

首次使用步骤：

1. 在"配置"中为默认用户 `homeassistant` 设置一个强密码。
2. 启动加载项，并在"日志"中查看是否启动成功。
3. 在 Home Assistant 中配置 `recorder` 集成，将 MariaDB 作为数据库后端。示例配置：

```yaml
recorder:
  db_url: mysql://homeassistant:password@core-mariadb/homeassistant?charset=utf8mb4
```

数据库文件持久化保存在 `/data/databases`，由 Home Assistant 的 `recorder` 和 `history` 组件使用。

## 常见问题

- **如何让 Home Assistant 使用 MariaDB？** 在 Home Assistant 配置中设置 `recorder.db_url`（格式如上），然后重启 Home Assistant。
- **为什么连不上 3306 端口？** 端口 3306 默认关闭，如需从外部访问，请在加载项"端口"设置中开放它。
- **升级到 3.0.0 需要注意什么？** 3.0.0 起 MariaDB 由 10.11 升级到 11.4，首次启动时会自动迁移数据库，请务必在升级前备份本加载项。

---
- 英文原版：Home Assistant App: MariaDB；链接 https://github.com/home-assistant/addons/blob/master/mariadb/README.md
- 来源仓库：official
