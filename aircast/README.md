<!-- zh-guide -->
# AirCast

## 简介

Apple 设备使用 AirPlay 协议向其他设备发送音频，但这与 Google 的 Chromecast 并不兼容。本加载项用于弥合这一兼容性差距：它会自动检测网络中的 Chromecast 播放器，并为每个播放器创建对应的虚拟 AirPlay 设备，作为 AirPlay 客户端与真实 Chromecast 播放器之间的桥接。AirCast 基于优秀的 [AirConnect](https://github.com/philippe44/AirConnect) 项目。

## 安装

1. 在 Home Assistant → 设置 → 加载项 → 商店，添加本商店仓库：
   - Gitee：https://gitee.com/zhqznc_10603234_123/ha-addon
   - GitHub：https://github.com/Treasoni/ha-addon-cn
2. 搜索 aircast 并安装。

## 配置

在加载项“配置”页修改配置后，需要重启加载项才能生效。可选配置键如下：

| 配置键 | 类型/默认值 | 说明 |
| ------ | ----------- | ---- |
| `log_level` | 可选 `list(trace|debug|info|notice|warning|error|fatal)`，默认 `空` | 日志输出详细程度：`trace` 输出全部细节；`debug` 输出调试信息；`info` 常规事件；`warning` 非错误的异常事件；`error` 运行时错误；`fatal` 致命错误。更高级别会自动包含更低级别的日志 |
| `address` | 可选 `str`，默认 `空` | 指定 AirCast 绑定的网络接口地址（IP），留空则监听所有接口 |
| `latency_rtp` | `int`，默认 `0` | RTP 音频流的延迟（毫秒） |
| `latency_http` | `int`，默认 `0` | HTTP 音频流的延迟（毫秒） |
| `drift` | `bool`，默认 `false` | 是否启用时钟漂移校正功能 |

## 使用 / 访问入口

本加载项没有 Web 界面，也不映射任何端口，它使用 host 网络模式运行以便发现网络中的 Chromecast 设备。安装并启动后，加载项会在局域网内为每个 Chromecast 播放器创建一个虚拟 AirPlay 设备。在支持 AirPlay 的 Apple 设备（如 iPhone、iPad、Mac）上打开“隔空播放”列表，即可看到并使用对应的 Chromecast 设备进行播放。

## 常见问题

- **修改配置后不生效？** AirCast 的配置（如延迟、漂移校正）修改后需要重启加载项才会生效。
- **隔空播放列表里看不到设备？** 请确认 Chromecast 播放器与 Home Assistant 处于同一局域网，且加载项已成功启动（可查看加载项日志确认运行状态）。
- **需要开放哪些端口？** 加载项使用 host 网络模式直接绑定主机的网络接口，因此无需在防火墙中额外开放端口。

---
- 英文原版：Home Assistant Community App: AirCast；链接 https://github.com/hassio-addons/repository/blob/main/aircast/README.md
- 来源仓库：frenck
