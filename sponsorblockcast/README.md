<!-- zh-guide -->
# CastSponsorSkip

## 简介

CastSponsorSkip 是一个用 Go 编写的程序，通过 SponsorBlock API 在本地所有 Chromecast 设备上自动跳过 YouTube 的赞助内容和可跳过的广告。它受 CastBlock 启发但从零编写，以避免其原有的一些缺陷。本加载项使用宿主网络模式，自动发现本地 Chromecast 设备并监控 YouTube 播放，跳过赞助内容。

## 安装

1. 在 Home Assistant → 设置 → 加载项 → 商店，添加本商店仓库：
   - Gitee：https://gitee.com/zhqznc_10603234_123/ha-addon
   - GitHub：https://github.com/Treasoni/ha-addon-cn
2. 搜索 `sponsorblockcast` 并安装。

## 配置

| 配置键 | 类型 / 默认值 | 说明 |
|--------|--------------|------|
| `CSS_CATEGORIES` | 字符串 / 空 | 要跳过的 SponsorBlock 分类（逗号分隔，默认 `sponsor, intro, outro, selfpromo`） |
| `CSS_DISCOVER_INTERVAL` | 字符串 / 空 | 重启 DNS 发现客户端的间隔（可选） |
| `CSS_MUTE_ADS` | 布尔 / 空 | 播放广告时将设备静音（可选） |
| `CSS_PAUSED_INTERVAL` | 字符串 / 空 | Cast 设备暂停时的轮询间隔（可选） |
| `CSS_PLAYING_INTERVAL` | 字符串 / 空 | Cast 设备播放时的轮询间隔（可选） |
| `CSS_YOUTUBE_API_KEY` | 字符串 / 空 | 用于兜底识别视频的 YouTube API 密钥（可选） |
| `env_vars` | 列表 / 空 | 额外环境变量列表（每项含 `name` 和 `value`），用于向容器传递自定义环境变量 |

## 使用 / 访问入口

该加载项没有网页界面，全部配置通过加载项选项完成。安装并启动后，它会自动发现本地 Chromecast 设备并监控 YouTube 播放，无需额外操作。

## 常见问题

- **适用场景**：它只在向 Chromecast 投屏 YouTube 视频时生效，能跳过多数赞助段落并减少手动操作，但无法跳过被强制观看的广告。
- **不适用场景**：在 Android TV 的原生 YouTube 应用中播放，或在手机上播放时，该程序不生效。
- **高级选项**：上游 CastSponsorSkip 项目还提供更多配置选项，可参考其官方文档按需通过 `env_vars` 传入。

---
- 英文原版：[CastSponsorSkip](https://github.com/alexbelgium/hassio-addons/blob/master/sponsorblockcast/README.md)
- 来源仓库：alexbelgium
