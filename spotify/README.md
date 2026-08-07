<!-- zh-guide -->
# Spotify Connect

## 简介

Spotify Connect 应用让你可以在运行 Home Assistant 的设备上播放 Spotify 音乐。它使用 Spotify Connect 协议，使你的设备成为一个可以被所有官方客户端控制的播放设备。例如，在树莓派上运行 Home Assistant 并安装本应用，即可让树莓派播放你的 Spotify 音乐，只需把音响系统接到树莓派即可。

## 安装

1. 在 Home Assistant 中进入「设置 → 加载项 → 商店」，点击右上角菜单添加本商店仓库：
   - Gitee：https://gitee.com/zhqznc_10603234_123/ha-addon
   - GitHub：https://github.com/Treasoni/ha-addon-cn
2. 在商店中搜索 `spotify`（Spotify Connect）并点击安装。
3. 选择音频输出设备并保存设置。
4. 启动应用并在日志中确认一切正常即可开始使用。

## 配置

> 注意：修改配置后需重启应用才会生效。

| 配置键 | 类型 / 默认值 | 说明 |
| --- | --- | --- |
| `log_level` | 枚举（trace\|debug\|info\|notice\|warning\|error\|fatal），可选 / 空 | 应用的日志输出级别。`trace` 显示全部细节，`debug` 显示详细调试信息，`info` 为正常事件，`warning` 为非错误的异常，`error` 为无需立即处理的错误，`fatal` 为致命错误。推荐使用 `info`。设为 `debug` 会同时开启 librespot 的调试模式。 |
| `name` | 字符串 / Home Assistant | 设备名称，即 Spotify Connect 目标名称，显示在官方 Spotify 客户端中。 |
| `bitrate` | 枚举（96\|160\|320） / 160 | Spotify 使用的码率。码率越高音质越好，但消耗更多流量。有效值为 `96`、`160`（默认）、`320`。 |
| `autoplay` | 布尔 / true | 队列播放完毕时，Spotify 是否自动播放相似歌曲。 |
| `initial_volume` | 字符串（匹配 0–100），可选 / 50 | 初始音量百分比（0–100）。在应用启动或崩溃恢复时生效。 |

## 使用 / 访问入口

本应用不提供 Web 界面，也不开放端口。启动后，它会在你的 Spotify 官方客户端中显示为一个可选择的播放设备，直接选择「Spotify Connect」设备即可把音乐投放到运行 Home Assistant 的设备上。

## 常见问题

- **需要 Spotify Premium 账号**：使用本应用需要 Spotify Premium 订阅。
- **客户端里看不到设备**：请确认应用已启动、配置了正确的音频输出，且你的手机/电脑与设备在同一网络。
- **音质不佳**：可在配置中把 `bitrate` 提高至 `320`（注意流量消耗也会增加）。
- **音量异常**：`initial_volume` 会在应用启动或崩溃恢复时重置音量，可设置为你常用的音量百分比。
- **不支持的登录方式**：早期版本的用户名/密码登录已被移除，请使用官方 Spotify 客户端控制播放。

---
- 英文原版：Spotify Connect；链接 https://github.com/hassio-addons/repository/blob/main/spotify/README.md
- 来源仓库：frenck
