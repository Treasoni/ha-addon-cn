<!-- zh-guide -->
# Guacamole Client

## 简介
Apache Guacamole 是一个无客户端的远程桌面网关，支持 VNC、RDP、SSH 等标准协议。它提供基于 Web 的界面，无需在用户设备上安装任何客户端软件即可访问远程系统，相当于在 Web 前端与实际远程桌面协议之间充当代理。本加载项整合了 Guacamole 服务器（guacd）与 Web 应用，并内置 PostgreSQL 数据库用于存储连接配置与用户管理，可随时通过浏览器安全访问你的电脑与服务器。

## 安装
1. 在 Home Assistant → 设置 → 加载项 → 商店，添加本商店仓库：
   - Gitee：https://gitee.com/zhqznc_10603234_123/ha-addon
   - GitHub：https://github.com/Treasoni/ha-addon-cn
2. 搜索 guacamole 并安装。

## 配置
| 配置键 | 类型 / 默认值 | 说明 |
|--------|---------------|------|
| `EXTENSIONS` | 字符串（可选） / `auth-totp` | 启用的 Guacamole 扩展，例如 `auth-totp`、`history-recording-storage` |
| `recording_search_path` | 字符串（可选） / `/config/recordings` | 历史录制存储扩展使用的录制搜索路径，对应 `guacamole.properties` 中的 `recording-search-path` |
| `TZ` | 字符串（可选） / 空 | 时区，例如 `Europe/London` |
| `env_vars` | 列表 / 空 | 额外环境变量（大写或小写命名） |
| `env_vars.name` | 字符串 | 环境变量名，须匹配 `^[A-Za-z0-9_]+$` |
| `env_vars.value` | 字符串（可选） | 环境变量值 |

## 使用 / 访问入口
启动后可在 Home Assistant 侧边栏看到 Guacamole Client 图标，点击进入。默认账号为 `guacadmin`、密码为 `guacadmin`，首次登录后请立即修改默认密码，然后通过 Web 界面添加 RDP、VNC 或 SSH 连接。

## 常见问题
1. 内置 PostgreSQL 数据库用于存储 Guacamole 的配置、用户与连接，数据库文件位于 `/config/postgres`，首次启动时自动创建。
2. `EXTENSIONS` 默认启用 `auth-totp`（TOTP 两步验证）；如需历史会话录制，可加入 `history-recording-storage` 并配合 `recording_search_path` 指定录制目录。
3. 需要手动认证时，在设置中为用户配置 TOTP；可通过 Web 界面创建更多用户并分配连接权限。

---
- 英文原版：Home assistant add-on: Guacamole；链接 https://github.com/alexbelgium/hassio-addons/blob/master/guacamole/README.md
- 来源仓库：alexbelgium
