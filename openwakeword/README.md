<!-- zh-guide -->
# openWakeWord

## 简介
本加载项基于 pyopen-wakeword，为 Home Assistant 提供本地唤醒词检测服务（Wyoming 协议），属于「语音之年」（Year of Voice）项目的一部分。你可以选择唤醒词并在设备本地监听，无需把音频发送到云端。

## 安装
1. 在 Home Assistant → 设置 → 加载项 → 商店，添加本商店仓库：
   - Gitee：https://gitee.com/zhqznc_10603234_123/ha-addon
   - GitHub：https://github.com/Treasoni/ha-addon-cn
2. 搜索 openwakeword 并安装。

## 配置
| 配置键 | 类型 / 默认值 | 说明 |
| --- | --- | --- |
| `threshold` | 浮点数 / `0.5` | 唤醒词检测的置信度阈值，数值越低越容易触发（也越容易误触发） |
| `trigger_level` | 整数 / `1` | 触发唤醒所需的连续检测次数，提高数值可减少误触发 |
| `debug_logging` | 布尔 / `false` | 是否输出调试日志 |

## 使用 / 访问入口
该加载项没有 Web 界面。启动后作为唤醒词检测服务（Wyoming 协议）监听端口 10400，供 Home Assistant 语音助手（Assist）调用。

## 常见问题
- **版本要求**：需要 Home Assistant 2023.9 或更高版本。
- **模型加载**：加载项会动态加载唤醒词模型，新放入的模型会自动被发现。
- **阈值调节**：误触发频繁时可适当提高 `threshold` 或 `trigger_level`；漏触发时可降低 `threshold`。

---
- 英文原版：Home Assistant App: openWakeWord（[链接](https://github.com/home-assistant/addons/blob/master/openwakeword/README.md)）
- 来源仓库：official
