<!-- zh-guide -->
# Maintainerr

## 简介
Maintainerr 是一个基于规则的媒体整理工具，适用于 Plex、Jellyfin 与 Emby 生态。它根据可配置规则（观看状态、入库时间、评分等）自动创建智能收藏，并可选择删除未观看内容，保持媒体库整洁；可对接 Sonarr/Radarr、Overseerr/Jellyseerr、Tautulli 等。

## 安装
1. 在 Home Assistant → 设置 → 加载项 → 商店，添加本商店仓库：
   - Gitee：https://gitee.com/zhqznc_10603234_123/ha-addon
   - GitHub：https://github.com/Treasoni/ha-addon-cn
2. 搜索 maintainerr 并安装。

## 配置

| 配置键 | 类型 / 默认值 | 说明 |
|--------|--------------|------|
| `TZ` | 字符串 / 默认 `Europe/London` | 时区，如 `Europe/Paris` |
| `env_vars` | 列表 / 默认 `[]` | 额外传给容器的环境变量（键名需匹配 `^[A-Za-z0-9_]+$`） |

可通过 `env_vars` 传入额外容器环境变量，例如 `UI_PORT`（更改监听端口）与 `BASE_PATH`（以子路径提供访问）。

## 使用 / 访问入口
- 通过浏览器访问宿主端口 6246 打开 Web 界面，在界面中配置媒体服务器与规则。

## 常见问题
- **配置会不会丢失？** 持久化数据（数据库、配置）保存在加载项配置目录中，升级或重装加载项后仍会保留。
- **如何修改访问端口或子路径？** 通过 `env_vars` 传入 `UI_PORT`（默认 6246）或 `BASE_PATH` 环境变量。

---
- 英文原版：[Home Assistant Add-on: Maintainerr](https://github.com/alexbelgium/hassio-addons/blob/master/maintainerr/README.md)
- 来源仓库：alexbelgium
