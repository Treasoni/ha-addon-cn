<!-- zh-guide -->
# Navidrome

## 简介
Navidrome 是一个开源、轻量的音乐服务器/流媒体服务，可自托管个人音乐库，兼容 Subsonic-API，支持多种客户端。本加载项对 Navidrome 做了多种配置增强，默认在 WebUI 中完成初始化。

## 安装
1. 在 Home Assistant → 设置 → 加载项 → 商店，添加本商店仓库：
   - Gitee：https://gitee.com/zhqznc_10603234_123/ha-addon
   - GitHub：https://github.com/Treasoni/ha-addon-cn
2. 搜索 navidrome 并安装。

## 配置

| 配置键 | 类型 / 默认值 | 说明 |
|--------|--------------|------|
| `base_url` | 字符串 / 默认 `/` | 反向代理下的基础 URL |
| `music_folder` | 字符串 / 默认 `/data/music` | 音乐库所在目录 |
| `data_folder` | 字符串 / 默认 `/data` | 应用数据（数据库）存放目录 |
| `log_level` | 字符串 / 默认 `info` | 日志级别：`error`、`warn`、`info`、`debug`、`trace` |
| `ssl` | 布尔 / 默认 `false` | 是否为 Web 界面启用 HTTPS |
| `certfile` | 字符串 / 默认 `fullchain.pem` | TLS 证书文件路径 |
| `keyfile` | 字符串 / 默认 `privkey.pem` | TLS 私钥文件路径 |
| `default_language` | 字符串（可选） | 界面默认语言 |
| `image_cache_size` | 字符串（可选） | 图片缓存大小 |
| `transcoding_cache_size` | 字符串（可选） | 转码缓存大小 |
| `scan_schedule` | 字符串（可选） | 自动扫描音乐库的 cron 表达式 |
| `password_encryption_key` | 字符串（可选） | 密码加密密钥 |
| `welcome_message` | 字符串（可选） | 自定义欢迎消息 |
| `lastfm_api_key` | 字符串（可选） | Last.fm API 密钥（用于 Scrobble） |
| `lastfm_secret` | 字符串（可选） | Last.fm 密钥 |
| `spotify_id` | 字符串（可选） | Spotify Client ID（用于元数据） |
| `spotify_secret` | 字符串（可选） | Spotify Client Secret |
| `localdisks` | 字符串（可选） | 要挂载的本地磁盘，如 `sda1,sdb1,MYNAS` |
| `networkdisks` | 字符串（可选） | 要挂载的 SMB 共享，如 `//SERVER/SHARE` |
| `cifsusername` | 字符串（可选） | SMB 网络共享用户名 |
| `cifspassword` | 字符串（可选） | SMB 网络共享密码 |
| `cifsdomain` | 字符串（可选） | SMB 网络共享域/工作组 |
| `env_vars` | 列表 / 默认 `[]` | 额外传给容器的环境变量（键名需匹配 `^[A-Za-z0-9_]+$`） |

## 使用 / 访问入口
- 通过浏览器访问宿主端口 4533 打开 Web 界面。
- 首次启动后先在 WebUI 中初始化应用，再重启加载项以应用部分选项。

## 常见问题
- **音乐文件放在哪里？** 默认读取 `/data/music`，可通过 `music_folder` 修改；也可用 `localdisks`/`networkdisks` 挂载外部存储。
- **如何开启 HTTPS？** 将 `ssl` 设为 `true`，并确保 `certfile`/`keyfile` 指向有效的证书文件。
- **如何定时扫描媒体库？** 通过 `scan_schedule` 设置 cron 表达式；还可配置 Last.fm 或 Spotify 集成以增强元数据与 Scrobble。

---
- 英文原版：[Home assistant add-on: Navidrome](https://github.com/alexbelgium/hassio-addons/blob/master/navidrome/README.md)
- 来源仓库：alexbelgium
