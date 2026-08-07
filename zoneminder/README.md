<!-- zh-guide -->
# Zoneminder

## 简介

Zoneminder 是一个功能完备、开源、技术先进的视频监控软件系统，用于连接并管理多个摄像头、录像、运动检测与报警。本加载项基于 [ZoneMinder 官方 Docker 镜像](https://github.com/ZoneMinder/zmdockerfiles)构建，数据库需要搭配 MariaDB 加载项使用。

## 安装

1. 在 Home Assistant → 设置 → 加载项 → 商店，添加本商店仓库：
   - Gitee：https://gitee.com/zhqznc_10603234_123/ha-addon
   - GitHub：https://github.com/Treasoni/ha-addon-cn
2. 搜索 zoneminder 并安装。
3. **安装并启动 MariaDB 加载项**，Zoneminder 需要 MySQL/MariaDB 数据库。
4. 保存配置并启动加载项，检查日志确认运行正常。

## 配置

所有配置项均可在加载项的「配置」页面编辑，保存并重启后生效。

| 配置键 | 类型 / 默认值 | 说明 |
|--------|--------------|------|
| `Images_location` | 字符串 / `/config/addons_config/zoneminder/images` | 摄像头图片存储路径 |
| `env_vars` | 对象列表 / `[]` | 附加环境变量列表（每项为 `name`/`value`，名称须匹配 `[A-Za-z0-9_]+`） |

## 使用 / 访问入口

- **Web 界面**：启动后访问 `http://homeassistant.local:3778/zm`（宿主端口 3778，把 `homeassistant.local` 换成你的 HA 主机地址即可）。
- **与 Home Assistant 集成**：可使用官方 [ZoneMinder 集成](https://www.home-assistant.io/integrations/zoneminder/)。

## 常见问题

- **数据库要求**：Zoneminder 需要 MySQL/MariaDB 数据库。请先安装 MariaDB 加载项，并在 Web 界面中配置数据库连接。
- **存储路径**：图片存储在 `Images_location` 指定的目录；事件（录像）存储在 `/var/cache/zoneminder/events2`，声音存储在 `/var/cache/zoneminder/sounds2`，配置在 `/config/addons_config/zoneminder`。
- **设置步骤**：启动后先通过 Web 界面连接摄像头，然后配置运动检测区域和报警规则，最后配置录像存储位置。

---
- 英文原版：Home assistant add-on: Zoneminder；链接 https://github.com/alexbelgium/hassio-addons/blob/master/zoneminder/README.md
- 来源仓库：alexbelgium
