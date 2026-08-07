<!-- zh-guide -->
# Free Games Claimer

## 简介
Free Games Claimer 基于 P-Adamiec/Free-Games-Claimer-Remaster，可自动领取以下商店的免费游戏：Epic Games 商店、Amazon Prime Gaming、GOG、Steam，以及在显式启用时的 GamerPower 支持的商店。为兼容旧版本，默认商店选择保持为 Epic Games、Prime Gaming 和 GOG。

## 安装
1. 在 Home Assistant → 设置 → 加载项 → 商店，添加本商店仓库：
   - Gitee：https://gitee.com/zhqznc_10603234_123/ha-addon
   - GitHub：https://github.com/Treasoni/ha-addon-cn
2. 搜索 free_games_claimer 并安装。

## 配置
| 配置键 | 类型 / 默认值 | 说明 |
|--------|---------------|------|
| `CONFIG_LOCATION` | 字符串 / `/config/config.env` | 持久化的环境配置文件路径 |
| `RUN_ONCE` | 布尔 / `true` | 运行所有选中的领取器一次后停止加载项（与旧版行为一致） |
| `STORES` | 字符串（可选） / 空 | 可选的逗号分隔商店覆盖，例如 `epic,prime,gog,steam` |
| `CMD_ARGUMENTS` | 字符串（可选） / `node epic-games ; node prime-gaming ; node gog` | 已废弃的兼容选项；识别的旧命令名会转换为 `STORES` |
| `env_vars` | 列表 / 空 | 额外环境变量（大写或小写命名） |
| `env_vars.name` | 字符串 | 环境变量名，须匹配 `^[A-Za-z0-9_]+$` |
| `env_vars.value` | 字符串（可选） | 环境变量值 |

配置保存在 `CONFIG_LOCATION`（默认 `/config/config.env`，在 Home Assistant 中位于加载项私有 addon_configs 目录），首次启动会生成模板。常用变量包括 `EG_EMAIL`、`EG_PASSWORD`、`PG_EMAIL`、`PG_PASSWORD`、`GOG_EMAIL`、`GOG_PASSWORD`、`NOTIFY` 等。

## 使用 / 访问入口
本加载项未启用 Ingress，通过端口访问：
- noVNC Web 界面：容器端口 `6080/tcp` 映射到宿主端口 `6080`（http://homeassistant:6080），可用于初始登录、验证码处理等手动浏览器操作。
- VNC 端口 `5900/tcp` 默认未映射到宿主端口。

## 常见问题
1. `RUN_ONCE: true`（默认）时加载项执行一次领取后停止；设为 `false` 时保持运行并使用内置调度器，在 `config.env` 中设置 `SCHEDULER_HOURS` 控制间隔。
2. 可在 `config.env` 中设置 `VNC_PASSWORD` 保护 VNC 会话。
3. 从 1.8 升级到 2.0 后，应用引擎从 vogler/free-games-claimer（Node.js + Firefox）切换为 P-Adamiec 版（Python + Chromium）；旧领取历史会在首次启动时自动迁移到 SQLite 数据库，需要交互认证的账户可能需要通过 noVNC 一次性登录，旧 Firefox 配置文件会保留且不会被删除。
4. 该加载项使用独立的 2.x 版本号并暂停自动上游更新，以避免版本回退，更新由维护者审核后进行。

---
- 英文原版：Home Assistant add-on: Free Games Claimer；链接 https://github.com/alexbelgium/hassio-addons/blob/master/free_games_claimer/README.md
- 来源仓库：alexbelgium
