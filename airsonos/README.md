<!-- zh-guide -->
# AirSonos

## 简介

Apple 设备使用 AirPlay 协议向其他设备发送音频，但这与 Sonos 播放器并不兼容。本加载项用于弥合这一兼容性差距：它会自动检测网络中的 Sonos 播放器，并为每个播放器创建对应的虚拟 AirPlay 设备，作为 AirPlay 客户端与真实 Sonos 设备之间的桥接。由于 Sonos 使用 UPnP，本加载项也可能兼容其他 UPnP 播放器（例如较新的三星电视）。AirSonos 基于优秀的 [AirConnect](https://github.com/philippe44/AirConnect) 项目。

## 安装

1. 在 Home Assistant → 设置 → 加载项 → 商店，添加本商店仓库：
   - Gitee：https://gitee.com/zhqznc_10603234_123/ha-addon
   - GitHub：https://github.com/Treasoni/ha-addon-cn
2. 搜索 airsonos 并安装。

## 配置

在加载项“配置”页修改配置后，需要重启加载项才能生效。可选配置键如下：

| 配置键 | 类型/默认值 | 说明 |
| ------ | ----------- | ---- |
| `log_level` | 可选 `list(trace|debug|info|notice|warning|error|fatal)`，默认 `info` | 日志输出详细程度：`trace` 输出全部细节；`debug` 输出调试信息；`info` 常规事件；`warning` 非错误的异常事件；`error` 运行时错误；`fatal` 致命错误。更高级别会自动包含更低级别的日志，默认 `info` 是推荐设置 |
| `address` | 可选 `str`，默认 `空` | 指定 AirSonos 服务器绑定的 IP 地址，留空时自动检测要使用的网络接口（多网卡环境下可能检测错误） |
| `port` | `port`，默认 `49152` | AirSonos 服务器对外暴露的端口，默认 `49152` 在大多数情况下够用，仅在确实必要时才修改 |
| `latency_rtp` | `int`，默认 `1000` | RTP（AirPlay）音频的缓冲时间（毫秒），用于缓解音频卡顿（如网络质量差时）；不建议低于 `500` |
| `latency_http` | `int`，默认 `2000` | HTTP 音频的缓冲时间（毫秒），用于缓解音频卡顿 |
| `drift` | `bool`，默认 `false` | 设为 `true` 可让计时参考产生漂移（无咔嗒声） |

## 使用 / 访问入口

本加载项没有 Web 界面，也不映射任何端口，它使用 host 网络模式运行以便发现网络中的 Sonos 播放器。安装并启动后，大约 30 秒后日志中会出现检测结果，此时在支持 AirPlay 的客户端（iOS、Mac、iTunes、Airfoil 等）上即可看到新的 AirPlay 设备，并可将音频播放到这些设备上。

## 常见问题

- **修改配置后不生效？** 所有配置（如端口、缓冲时间、日志级别）修改后都需要重启加载项才会生效。
- **为什么看不到某个 Sonos 设备？** 当创建 Sonos 分组时，只有组主设备会显示为 AirPlay 播放器，其他已检测到的成员会被移除；分组解散后各设备会重新出现。每次检测周期约为 30 秒。
- **音量如何调节？** 音量是针对整个 Sonos 组设置的，所有成员音量相同；如需单独调节某个成员的音量，需使用 Sonos 原生控制器，且之后从 AirPlay 设备更改组音量会覆盖这些单独设置。
- **播放时卡顿怎么办？** 可适当增大 `latency_rtp` 和 `latency_http` 的缓冲时间（毫秒），修改后重启加载项；`latency_rtp` 不建议低于 `500`。

---
- 英文原版：Home Assistant Community App: AirSonos；链接 https://github.com/hassio-addons/repository/blob/main/airsonos/README.md
- 来源仓库：frenck
