<!-- zh-guide -->
# Whisper

## 简介
Whisper 是一个基于 Whisper 的本地语音转文字（Speech-to-text）加载项，支持多种语音识别后端：faster-whisper、HuggingFace transformers、sherpa-onnx（仅 parakeet 模型）和 onnx-asr（仅 GigaAM）。它是 Home Assistant 官方「语音之年（Year of Voice）」项目的一部分，通过 Wyoming 协议被 Home Assistant 自动发现，可为语音助手（Assist）提供本地语音转文字能力。

## 安装
1. 在 Home Assistant → 设置 → 加载项 → 加载项商店，添加本商店仓库：
   - Gitee：https://gitee.com/zhqznc_10603234_123/homeassistant
   - GitHub：https://github.com/Treasoni/ha-addon-cn
2. 搜索 whisper 并安装。

## 配置
以下是 config.yaml 中真实的配置项。表格按「配置键 | 类型/默认值 | 说明」排列：

| 配置键 | 类型/默认值 | 说明 |
| --- | --- | --- |
| `model` | 下拉列表 / `auto` | 用于转写的 Whisper 模型。`auto` 会根据 CPU 自动选择：ARM 设备（如树莓派 4）用 `tiny-int8`，其余用 `base-int8`。可选 `tiny`/`base`/`small`/`medium`/`large`/`turbo` 等（含 `int8` 压缩版与 `distil` 蒸馏版），选 `custom` 则使用 `custom_model` 指定的模型 |
| `language` | 下拉列表 / `en` | 预加载模型的默认语言。选 `auto` 会自动检测说话语言，但运行会**明显变慢**；自 Home Assistant 2023.8 起，不同 Assist 语音流程可同时使用多种语言 |
| `beam_size` | 整数 / `0` | 转写时同时考虑的候选数量（束搜索）。`0` 表示自动：ARM 设备取 1，其余取 5。增大可提升准确率但降低性能 |
| `custom_model_type` | 下拉列表 / `faster-whisper` | 当 `stt_library` 为 `auto` 且启用了 `custom_model` 时，决定所用的语音识别后端（faster-whisper / sherpa / transformers / onnx-asr / funasr） |
| `stt_library` | 下拉列表 / `auto` | 语音识别后端库：`auto`（按语言/硬件自动选择）、`faster-whisper`、`sherpa`（仅 parakeet 模型）、`transformers`、`onnx-asr`、`funasr`。注意：设置了 `custom_model` 时，`custom_model_type` 会覆盖 `stt_library` 的 `auto` 选择 |
| `whisper_task` | 下拉列表 / `transcribe` | 模型执行的任务：`transcribe`（按原语言转写，默认）、`translate`（翻译成英文） |
| `sherpa_streaming` | 布尔 / `false` | 配合 `sherpa` 后端使用流式模型。会用一个更快但准确率略低的流式模型（sherpa-onnx-streaming-zipformer）替换默认英文模型（parakeet） |
| `vad_clip` | 布尔 / `false` | 转写前用语音活动检测（VAD）裁剪掉静音片段。主要对含较多静音的音频和按长度分批的后端（如 `sherpa`、`funasr`）有延迟收益；流式后端不受影响 |
| `local_files_only` | 布尔 / `false` | 只使用已下载的模型，不再联网检查更新。首次使用模型前请保持关闭以完成下载；模型下载完成后可开启，让加载项完全离线并跳过每次请求的更新检查（也加快启动）。若在模型下载前开启，转写会失败直到关闭或切换为已下载的模型 |
| `debug_logging` | 布尔 / `false` | 在加载项日志中输出 DEBUG 级别信息 |
| `custom_model`（可选） | 字符串 / 无默认值 | 本地已转换模型目录的路径，或 HuggingFace Hub 上的 CTranslate2 转换版 Whisper 模型 ID（如 `Systran/faster-distil-whisper-small.en`）。`custom_model_type` 为 `transformers` 时需填写 transformers 版模型 ID（如 `openai/whisper-tiny.en`）。本地模型路径必须以 `/config/models/` 开头 |
| `initial_prompt`（可选） | 字符串 / 无默认值 | 音频内容描述，可帮助 Whisper 更好地转写生僻词 |

## 使用 / 访问入口
- 加载项启动后会在容器内监听 `tcp://0.0.0.0:10300`（Wyoming 协议）；`10300/tcp` 端口默认不对宿主机开放。
- Home Assistant 的 Wyoming 集成会自动发现本加载项，无需手动配置；也可以手动添加 Wyoming 集成，协议地址为 `tcp://<主机地址>:10300`。
- 配置完成后，在语音助手（Assist）的语音处理流程中选择 Whisper 作为语音转文字引擎即可开始使用。
- 语言与优先级推荐（`stt_library` = `auto` 时自动按语言/硬件选择）：
  - 英文（`en`）：默认走 sherpa 后端的 parakeet 模型；`sherpa_streaming` 可切换为更快的流式版本。
  - 中文 / 粤语 / 日语 / 韩语（`zh` / `yue` / `ja` / `ko`）：走 funasr 后端的 SenseVoice 模型，比 Whisper 明显更快且对这些语言支持良好（`zh-CN` / `zh-TW` / `zh-HK` 等地区码会自动映射）。
  - 俄语（`ru`）：走 onnx-asr 后端的 GigaAM 模型。
  - 其他语言：默认使用 faster-whisper。
  - 非英文建议把 `language` 设为明确的语言代码（`auto` 会显著变慢）；想把非英文语音输出为英文文本时，把 `whisper_task` 设为 `translate`（仅对 Whisper 系列后端有效，parakeet/sherpa、SenseVoice、GigaAM 不支持）。

## 常见问题
1. **选 `language` = `auto` 为什么很慢？** 模型每次请求都要先检测说话语言，因此运行会明显变慢；建议明确设置语言代码。
2. **如何配置本地自定义模型？** 在加载项配置目录下创建 `models` 子目录，把模型目录复制到 `/addon_configs/core_whisper/models/<模型目录>`，然后将 `custom_model` 设为 `/config/models/<模型目录>`，且路径必须以 `/config/models/` 开头。
3. **为什么备份里没有模型文件？** Whisper 模型文件较大，会被自动排除在备份之外；远程模型在恢复后会自动重新下载。若恢复备份时用的是本地自定义模型，需要手动重新复制模型目录。
4. **`local_files_only` 开启后转写失败？** 说明模型还没下载完成。先关闭该选项完成模型下载，再开启它即可保持离线运行。

---
- 英文原版：Home Assistant App: Whisper；链接 https://github.com/home-assistant/addons/blob/master/whisper/README.md
- 来源仓库：official
