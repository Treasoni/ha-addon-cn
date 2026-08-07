<!-- zh-guide -->
# Piper

## 简介
Piper 是一个本地文本转语音（Text-to-Speech）加载项，基于 [Piper](https://github.com/OHF-Voice/piper1-gpl) 引擎，将文字合成自然的语音。它是 Home Assistant [语音之年（Year of Voice）](https://www.home-assistant.io/blog/2022/12/20/year-of-voice/)计划的一部分，语音数据在本地处理，无需云端服务。

## 安装
1. 在 Home Assistant → 设置 → 加载项 → 商店，添加本商店仓库：
   - Gitee：https://gitee.com/zhqznc_10603234_123/ha-addon
   - GitHub：https://github.com/Treasoni/ha-addon-cn
2. 搜索 piper 并安装。

## 配置
| 配置键 | 类型/默认值 | 说明 |
| --- | --- | --- |
| voice | 字符串，默认 `en_US-lessac-medium` | 使用的 Piper 语音名称，支持几十种语言的数百个音色（含中文语音）；语音模型启动时自动从 https://huggingface.co/rhasspy/piper-voices 下载。命名格式为 `<语言>_<地区>-<人名>-<质量>`，质量等级：`x_low`（16kHz，最小最快）、`low`（16kHz，快）、`medium`（22.05kHz，较慢但音质更好）、`high`（22.05kHz，最慢但音质最好） |
| speaker | 整数，默认 `0` | 当语音支持多个说话人时，指定使用第几个说话人（默认使用第一个） |
| length_scale | 浮点数，默认 `1.0` | 语速调节：`1.0` 为默认语速，`< 1.0` 更快，`> 1.0` 更慢 |
| noise_scale | 浮点数，默认 `0.667` | 通过在生成时加入噪声控制音频的变化程度；`0` 表示无变化，大于 `1` 会开始损伤音质 |
| noise_w | 浮点数，默认 `0.333` | 控制说话节奏（音素时长）的变化程度；`0` 表示无变化，大于 `1` 会出现明显的停顿/口吃 |
| sentence_silence | 浮点数，默认 `0.0` | 每句话结束后追加的静音秒数 |
| debug_logging | 布尔，默认 `false` | 在加载项日志中输出 DEBUG 级别的调试信息 |
| update_voices | 布尔，默认 `true` | 每次加载项启动时自动下载最新语音列表；需在 Home Assistant 中重新加载 Piper 的 Wyoming 集成才能看到新语音 |

> 说明：在 Raspberry Pi 4 上，`medium` 及以下质量的模型可以流畅运行；如果对音质要求不高，优先选择 `low` 或 `x_low`，速度会明显更快。

## 使用 / 访问入口
- Piper 通过 **Wyoming 协议**（端口 `10200/tcp`）对外提供服务，安装并启动后会被 Home Assistant 的 Wyoming 集成自动发现。
- 完成接入：点击 [my.home-assistant.io 配置入口](https://my.home-assistant.io/redirect/config_flow_start/?domain=wyoming) 一键添加，或在“设置 → 设备与服务”中手动添加 **Wyoming** 集成（参见 [Wyoming 集成文档](https://www.home-assistant.io/integrations/wyoming/)）。
- 常用操作：在加载项“配置”中选择语音（可先试听 https://rhasspy.github.io/piper-samples/ 上的音色示例）、调整语速/音调，然后在 Home Assistant 的 TTS 服务中调用 Piper 播放文字。
- **自定义语音**：把自定义语音文件放到 `/share/piper` 目录，每个语音需包含模型文件（`<voice>.onnx`）和配置文件（`<voice>.onnx.json`）。训练方法见 [Piper 训练指南](https://github.com/rhasspy/piper/blob/master/TRAINING.md)。

## 常见问题
1. **想用中文语音怎么办？** 在 `voice` 配置项中选择中文音色即可，例如 `zh_CN-huayan-medium`、`zh_CN-chaowen-medium`、`zh_CN-xiao_ya-medium` 等。
2. **更新语音列表后看不到新语音？** 开启 `update_voices` 后，还需在 Home Assistant 中重新加载（重载）Piper 对应的 Wyoming 集成才能刷新语音列表。
3. **首次使用需要联网吗？** 需要——语音模型在首次使用时从 Hugging Face 下载，之后在本地运行；建议预置带宽和存储空间（模型按质量等级大小不同）。

---
- 英文原版：Home Assistant App: Piper；链接 https://github.com/home-assistant/addons/blob/master/piper/README.md
- 来源仓库：official
