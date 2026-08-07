<!-- zh-guide -->
# Kometa

## 简介
Kometa（原 Plex Meta Manager）是一个 Python 3 脚本，通过 YAML 配置文件按计划持续更新电影、剧集与收藏夹的元数据，并可根据各种规则自动构建收藏，详细说明见其官方 wiki。本加载项基于 linuxserver/docker-kometa 镜像构建。

## 安装
1. 在 Home Assistant → 设置 → 加载项 → 商店，添加本商店仓库：
   - Gitee：https://gitee.com/zhqznc_10603234_123/ha-addon
   - GitHub：https://github.com/Treasoni/ha-addon-cn
2. 搜索 kometa 并安装。

## 配置
配置可通过加载项选项与 `config.yml` 两种方式完成；进阶用法可把额外的环境变量放入 `config.yml` 所在位置，详见 Kometa wiki 的环境变量清单。

| 配置键 | 类型 / 默认值 | 说明 |
|--------|--------------|------|
| `PUID` | 整数 / 默认 `0` | 文件权限的用户 ID |
| `PGID` | 整数 / 默认 `0` | 文件权限的用户组 ID |
| `TZ` | 字符串（可选） | 时区，如 `Europe/London` |
| `KOMETA_CONFIG` | 字符串 / 默认 `/config/addons_config/kometa/config.yml` | Kometa 配置文件路径，可指定自定义配置文件 |
| `KOMETA_TIME` | 字符串（可选） | 每日更新时刻，格式 `HH:MM`，多个用逗号分隔 |
| `KOMETA_RUN` | 布尔（可选） | 设为 true 时跳过调度、直接运行一次 |
| `KOMETA_TEST` | 布尔（可选） | 设为 true 时进入调试模式，仅处理标记了 `test: true` 的收藏 |
| `KOMETA_NO_MISSING` | 布尔（可选） | 设为 true 时跳过缺失影片/剧集相关功能 |
| `env_vars` | 列表 / 默认 `[]` | 额外传给容器的环境变量（键名需匹配 `^[A-Za-z0-9_]+$`） |

## 使用 / 访问入口
- 本加载项没有 Web 界面；Kometa 会按 `KOMETA_TIME` 的计划定时运行，也可通过 `KOMETA_RUN: true` 立即运行一次。
- 运行情况可在加载项日志中查看。

## 常见问题
- **如何快速上手？** 可参考 Kometa 官方的初始配置文件 walkthrough 教程，先准备好 `config.yml` 并设置 `KOMETA_CONFIG` 指向它。
- **只想手动运行一次？** 将 `KOMETA_RUN` 设为 `true` 启动即可跳过调度；`KOMETA_TEST` 用于仅调试标记了 `test: true` 的收藏。
- **有哪些可用的环境变量？** 完整的 Kometa 环境变量清单见官方 wiki 的 environmental 页面，也可通过 `env_vars` 传入额外的变量。

---
- 英文原版：[Home assistant add-on: Kometa](https://github.com/alexbelgium/hassio-addons/blob/master/kometa/README.md)
- 来源仓库：alexbelgium
