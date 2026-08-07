<!-- zh-guide -->
# Seerr

## 简介

Seerr 是一个开源的媒体请求与发现管理器，用于 Jellyfin、Plex 和 Emby。用户可以在其中搜索电影与剧集并发起观看请求，再交由下载与媒体管理工具处理。本加载项基于 Overseerr 的加载项结构改造，适配 Seerr 上游项目与容器镜像，并通过内部 NGINX 反向代理支持 Home Assistant Ingress。

## 安装

1. 在 Home Assistant → 设置 → 加载项 → 商店，添加本商店仓库：
   - Gitee：https://gitee.com/zhqznc_10603234_123/ha-addon
   - GitHub：https://github.com/Treasoni/ha-addon-cn
2. 搜索 `seerr` 并安装。

## 配置

| 配置键 | 类型 / 默认值 | 说明 |
|--------|--------------|------|
| `NODE_MEMORY_LIMIT` | 整数 / 默认 `512` | Node.js 堆内存上限（MB）。媒体库很大导致 Seerr 崩溃时调大，内存紧张时可调小 |
| `env_vars` | 列表 / 空 | 额外环境变量列表（每项含 `name` 和 `value`），用于向容器传递自定义环境变量 |
| `PGID` | 整数 / 默认 `0` | 文件权限组 ID |
| `PUID` | 整数 / 默认 `0` | 文件权限用户 ID |
| `TZ` | 字符串 / 空 | 时区（如 `Europe/London`） |

## 使用 / 访问入口

启动后可在 Home Assistant 侧边栏看到 Seerr 图标，点击进入。也可通过宿主端口 5055 直接访问 Web 界面。

## 常见问题

- **从 Overseerr 迁移**：Seerr 兼容 Overseerr 的数据格式。先安装并启动一次 Seerr 生成配置目录 `/addon_configs/db21ed7f_seerr/`，再停止；然后用 Filebrowser 把 `/addon_configs/db21ed7f_overseerr/` 下的文件全部复制到 Seerr 的配置目录，最后启动 Seerr 即可保留原有设置、用户和请求。
- **从 Jellyseerr 迁移**：操作方式与 Overseerr 相同，把 `/addon_configs/db21ed7f_jellyseerr/` 的文件复制到 `/addon_configs/db21ed7f_seerr/`。
- **从 Ombi 迁移**：Ombi 数据格式不同，没有自动迁移路径，需要手动记录媒体服务器、用户与通知设置，再在 Seerr 界面重新配置。
- **搜索含特殊字符的标题**：通过 Ingress 搜索如 `Monsters, Inc.`、`Ocean's Eleven` 等含特殊字符的标题时，NGINX 已做重新编码处理；直接使用 5055 端口不受影响。
- **内存设置**：库较大或出现 OOM 导致加载项无响应时，可适当增大 `NODE_MEMORY_LIMIT`。

---
- 英文原版：[Seerr](https://github.com/alexbelgium/hassio-addons/blob/master/seerr/README.md)
- 来源仓库：alexbelgium
