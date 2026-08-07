<!-- zh-guide -->
# Requestrr

## 简介

Requestrr 是一个聊天机器人，用于通过聊天的方式简化 Sonarr、Radarr、Ombi 等服务的使用。当前仅支持 Discord 平台，但设计上便于快速扩展新功能和新平台。本加载项基于 linuxserver/docker-requestrr 镜像构建。

## 安装

1. 在 Home Assistant → 设置 → 加载项 → 商店，添加本商店仓库：
   - Gitee：https://gitee.com/zhqznc_10603234_123/ha-addon
   - GitHub：https://github.com/Treasoni/ha-addon-cn
2. 搜索 `requestrr` 并安装。

## 配置

主要配置可直接在应用网页界面中完成，以下选项可在加载项配置中设置。

| 配置键 | 类型 / 默认值 | 说明 |
|--------|--------------|------|
| `env_vars` | 列表 / 空 | 额外环境变量列表（每项含 `name` 和 `value`），用于向容器传递自定义环境变量 |
| `PGID` | 整数 / 默认 `0` | 文件权限组 ID |
| `PUID` | 整数 / 默认 `0` | 文件权限用户 ID |
| `TZ` | 字符串 / 空 | 时区（如 `Europe/London`） |

## 使用 / 访问入口

启动后通过浏览器访问宿主端口 4545（Web 界面）。默认用户名与密码见加载项启动日志，首次运行后可在配置目录中的配置文件内修改。

## 常见问题

- **默认账号密码在哪**：默认用户名与密码会打印在加载项启动日志中。建议先启动一次加载项，再用 Filebrowser 修改 `/addon_configs/db21ed7f_requestrr` 下的配置文件。
- **配置文件位置**：自 2.1.6 起配置从 `/config/hassio_addons/requestrr` 迁移到 `/addon_configs/db21ed7f_requestrr`（仅可通过 Filebrowser 加载项访问），迁移与自定义脚本会自动处理，请更新相关链接。
- **如何添加自定义环境变量**：可通过 `env_vars` 选项向容器传递额外的环境变量。

---
- 英文原版：[Requestrr](https://github.com/alexbelgium/hassio-addons/blob/master/requestrr/README.md)
- 来源仓库：alexbelgium
