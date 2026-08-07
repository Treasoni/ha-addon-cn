<!-- zh-guide -->
# Speech-to-Phrase

## 简介
本加载项提供一个快速、完全本地的语音转文字（语音到短语）系统，并且会用你家中实体的名称进行个性化。它针对较低端的硬件（如树莓派 4 与 Home Assistant Green）做了优化，可用于本地语音命令识别。

## 安装
1. 在 Home Assistant → 设置 → 加载项 → 商店，添加本商店仓库：
   - Gitee：https://gitee.com/zhqznc_10603234_123/ha-addon
   - GitHub：https://github.com/Treasoni/ha-addon-cn
2. 搜索 speech_to_phrase 并安装。

## 配置
| 配置键 | 类型 / 默认值 | 说明 |
| --- | --- | --- |
| `debug_logging` | 布尔 / `false` | 是否输出调试日志 |

## 使用 / 访问入口
该加载项没有 Web 界面。启动后作为本地语音转文字服务（Wyoming 协议）监听端口 10300，供 Home Assistant 语音助手（Assist）调用。

## 常见问题
- **版本要求**：需要 Home Assistant 2023.11 或更高版本。
- **可用的语音命令**：支持的语音命令见上游 speech-to-phrase 项目的文档。
- **个性化**：加载项会用家中实体的名称来个性化识别结果，因此识别更贴合你的家庭环境。
- **目标硬件**：针对树莓派 4 与 Home Assistant Green 等低端硬件做了优化。

---
- 英文原版：Home Assistant App: Speech to phrase（[链接](https://github.com/home-assistant/addons/blob/master/speech_to_phrase/README.md)）
- 来源仓库：official
