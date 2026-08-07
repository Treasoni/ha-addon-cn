<!-- zh-guide -->
# Social to Mealie

## 简介

Social to Mealie 可以将社交媒体视频中的菜谱直接导入到你的 Mealie 实例中。它通过 AI 转录视频内容并整理成结构化菜谱，保存到 Mealie。本加载项基于 social-to-mealie 项目镜像构建。

## 安装

1. 在 Home Assistant → 设置 → 加载项 → 商店，添加本商店仓库：
   - Gitee：https://gitee.com/zhqznc_10603234_123/ha-addon
   - GitHub：https://github.com/Treasoni/ha-addon-cn
2. 搜索 `social_to_mealie` 并安装。

## 配置

| 配置键 | 类型 / 默认值 | 说明 |
|--------|--------------|------|
| `OPENAI_URL` | 字符串 / 默认 `https://api.openai.com/v1` | OpenAI 兼容接口的地址 |
| `OPENAI_API_KEY` | 字符串 / 空 | OpenAI 兼容接口的 API 密钥 |
| `TRANSCRIPTION_MODEL` | 字符串 / 默认 `whisper-1` | 用于音频转录的 Whisper 模型 |
| `TEXT_MODEL` | 字符串 / 默认 `gpt-4o-mini` | 用于生成菜谱的文本模型 |
| `MEALIE_URL` | 字符串 / 空 | 你的 Mealie 实例地址 |
| `MEALIE_API_KEY` | 字符串 / 空 | Mealie 的 API 密钥 |
| `MEALIE_GROUP_NAME` | 字符串 / 默认 `home` | Mealie 分组名（可选） |
| `YTDLP_VERSION` | 字符串 / 默认 `latest` | 启动时下载的 yt-dlp 版本 |
| `EXTRA_PROMPT` | 字符串 / 空 | 附加给 AI 的额外指令（可选） |
| `COOKIES` | 字符串 / 空 | 供 yt-dlp 访问受保护社交媒体内容的 cookies 字符串（可选） |
| `env_vars` | 列表 / 空 | 额外环境变量列表（每项含 `name` 和 `value`） |

## 使用 / 访问入口

Web 界面位于宿主端口 3000。

## 常见问题

- **依赖要求**：需要 Mealie 1.9.0 及以上版本，并在 Mealie 中配置了 AI 提供方。
- **预下载 yt-dlp**：可通过设置 `YTDLP_VERSION`（例如 `latest` 或具体版本号）在启动时预先下载 yt-dlp。
- **受保护内容**：如果社交媒体的视频内容需要登录才能访问，可通过 `COOKIES` 选项提供 cookies 字符串供 yt-dlp 使用。

---
- 英文原版：[Social to Mealie](https://github.com/alexbelgium/hassio-addons/blob/master/social_to_mealie/README.md)
- 来源仓库：alexbelgium
