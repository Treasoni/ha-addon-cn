<!-- zh-guide -->
# Spotify to Plex

## 简介

Spotify to Plex 可以自动将你的 Spotify 播放列表同步到 Plex 媒体库：支持同步任意 Spotify 播放列表（包括 Spotify 官方列表）、多个 Spotify 用户、定时自动同步、智能缓存，并可选择通过 Lidarr、SLSKD 或 Tidal 下载缺失的曲目。本加载项基于 jjdenhertog/spotify-to-plex 镜像构建。

## 安装

1. 在 Home Assistant → 设置 → 加载项 → 商店，添加本商店仓库：
   - Gitee：https://gitee.com/zhqznc_10603234_123/ha-addon
   - GitHub：https://github.com/Treasoni/ha-addon-cn
2. 搜索 `spotify_to_plex` 并安装。

## 配置

启动前你需要一个 Spotify 开发者应用（https://developer.spotify.com/dashboard）：创建应用并记下其 `Client ID` 和 `Client Secret`，然后在应用设置中把回调地址 `SPOTIFY_API_REDIRECT_URI` 的值添加到重定向 URI 列表。

| 配置键 | 类型 / 默认值 | 说明 |
|--------|--------------|------|
| `SPOTIFY_API_CLIENT_ID` | 字符串 / 空 | Spotify 开发者应用的 Client ID |
| `SPOTIFY_API_CLIENT_SECRET` | 字符串 / 空 | Spotify 开发者应用的 Client Secret |
| `SPOTIFY_API_REDIRECT_URI` | 字符串 / 默认 `https://jjdenhertog.github.io/spotify-to-plex/callback.html` | OAuth 回调地址，需与 Spotify 应用中配置的一致 |
| `ENCRYPTION_KEY` | 字符串 / 空 | 用于加密存储的密钥。留空则在首次启动时自动生成并保存在加载项配置目录；如需复用已有配置再自行指定 |
| `env_vars` | 列表 / 空 | 额外环境变量列表（每项含 `name` 和 `value`），用于传递 Tidal、SLSKD、Lidarr、Plex 等上游设置 |

## 使用 / 访问入口

Web 界面位于宿主端口 9030，启动后在其中完成 Spotify 与 Plex 账号的授权连接。

## 常见问题

- **配置与缓存**：配置和缓存存放在加载项配置目录中，重启与更新后仍然保留。
- **回调地址**：`SPOTIFY_API_REDIRECT_URI` 的默认值对应上游提供的回调页面；只有当你自行托管回调页时才需要修改。
- **同步能力**：支持同步包括 Spotify 官方播放列表在内的任意播放列表，并支持多个 Spotify 用户与定时自动同步。

---
- 英文原版：[Spotify to Plex](https://github.com/alexbelgium/hassio-addons/blob/master/spotify_to_plex/README.md)
- 来源仓库：alexbelgium
