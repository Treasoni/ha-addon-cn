<!-- zh-guide -->
# SQLite Web

## 简介

SQLite Web 让你可以直接在 Web 浏览器中浏览 Home Assistant 的 SQLite 数据库。你可以轻松查看数据库中保存的所有数据表和内容，非常适合排查与了解 Home Assistant 的历史数据。

## 安装

1. 在 Home Assistant 中进入「设置 → 加载项 → 商店」，点击右上角菜单添加本商店仓库：
   - Gitee：https://gitee.com/zhqznc_10603234_123/ha-addon
   - GitHub：https://github.com/Treasoni/ha-addon-cn
2. 在商店中搜索 `sqlite-web`（SQLite Web）并点击安装。
3. 启动应用并在日志中确认一切正常。
4. 打开 Web 界面，使用你的 Home Assistant 用户登录。

## 配置

> 注意：修改配置后需重启应用才会生效。

| 配置键 | 类型 / 默认值 | 说明 |
| --- | --- | --- |
| `database` | 字符串，可选 / 空 | 指定要打开的数据库文件路径。未设置时使用 Home Assistant 默认的数据库文件位置。 |

## 使用 / 访问入口

启动后可在 Home Assistant 侧边栏看到 SQLite Web 图标，点击进入即可打开数据库浏览界面，并使用你的 Home Assistant 账号登录。

## 常见问题

- **登录方式**：请使用你的 Home Assistant 用户账号登录，而不是单独设置密码。
- **查看特定数据库**：如需浏览非默认的数据库文件，可在配置中设置 `database` 为对应的数据库文件路径。
- **只读操作建议**：SQLite Web 面向浏览与排查历史数据，进行写操作前请确保已备份数据库。

---
- 英文原版：SQLite Web；链接 https://github.com/hassio-addons/repository/blob/main/sqlite-web/README.md
- 来源仓库：frenck
