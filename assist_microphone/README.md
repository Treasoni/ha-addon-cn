<!-- zh-guide -->
# Assist Microphone

## 简介
本加载项通过本地 USB 麦克风为 Home Assistant 的 Assist 语音助手提供语音控制能力（基于 Wyoming 协议，上游为 wyoming-satellite），属于「语音之年」（Year of Voice）项目的一部分。

> [!CAUTION]
> 该加载项已弃用（deprecated），上游 Wyoming Satellite 项目已停止维护，建议迁移到功能更丰富的 [Assist Satellite](https://github.com/OHF-Voice/apps/tree/main/assist_satellite) 应用。

## 安装
1. 在 Home Assistant → 设置 → 加载项 → 商店，添加本商店仓库：
   - Gitee：https://gitee.com/zhqznc_10603234_123/ha-addon
   - GitHub：https://github.com/Treasoni/ha-addon-cn
2. 搜索 assist_microphone 并安装。

## 配置
| 配置键 | 类型 / 默认值 | 说明 |
| --- | --- | --- |
| `awake_wav` | 字符串 / `/usr/src/sounds/awake.wav` | 唤醒时提示音 WAV 文件的路径 |
| `done_wav` | 字符串 / `/usr/src/sounds/done.wav` | 语音处理完成时提示音 WAV 文件的路径 |
| `timer_finished_wav` | 字符串 / `/usr/src/sounds/timer_finished.wav` | 定时器结束时提示音 WAV 文件的路径 |
| `timer_repeat_count` | 整数 / `3` | 定时器结束时提示音重复播放的次数 |
| `timer_repeat_delay` | 浮点数 / `0.75` | 定时器结束时提示音重复播放的间隔（秒） |
| `sound_enabled` | 布尔 / `true` | 是否播放提示音 |
| `noise_suppression` | 整数 / `0` | 噪声抑制级别，`0` 表示关闭 |
| `auto_gain` | 整数 / `0` | 麦克风自动增益级别，`0` 表示关闭 |
| `mic_volume_multiplier` | 浮点数 / `1.0` | 麦克风音量倍率 |
| `sound_volume_multiplier` | 浮点数 / `1.0` | 声音输出音量倍率 |
| `debug_logging` | 布尔 / `false` | 是否输出调试日志 |

## 使用 / 访问入口
该加载项没有 Web 界面，也没有对外端口。启动后作为本地语音服务（Wyoming 协议）运行，配合 Home Assistant 的 Assist 语音助手，使用本地 USB 麦克风进行语音控制。

## 常见问题
- **加载项已弃用**：Assist Microphone 已停止维护，请迁移到 [Assist Satellite](https://github.com/OHF-Voice/apps/tree/main/assist_satellite) 以获得更新的版本和更多功能。
- **定时器功能**：v1.3.0 起支持定时器，可配置定时器结束的提示音文件、重复次数与间隔。
- **提示音文件**：三个提示音路径默认指向加载项内置的 `/usr/src/sounds/` 目录；如需自定义，请替换为实际存在的 WAV 文件路径。

---
- 英文原版：[DEPRECATED] Home Assistant App: Assist Microphone（[链接](https://github.com/home-assistant/addons/blob/master/assist_microphone/README.md)）
- 来源仓库：official
