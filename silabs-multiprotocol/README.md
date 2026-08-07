<!-- zh-guide -->
# Silicon Labs Multiprotocol [deprecated]

## 简介
本加载项可在一颗 Silicon Labs 无线芯片（如 Home Assistant Yellow、SkyConnect 与 Connect ZBT-1 内置的芯片）上同时使用 Zigbee 和 OpenThread 两种协议。无线模块需要安装支持多个 IEEE 802.15.4 PAN 的 RCP Multi-PAN 固件（已在 EFR32 Series 2 芯片上测试）。

> [!CAUTION]
> 多协议（multiprotocol）已不再受支持，且将很快被移除。请参考 Connect ZBT-1 文档中的「禁用多协议」流程，把无线模块刷回纯 Zigbee 或 Thread 固件。

## 安装
1. 在 Home Assistant → 设置 → 加载项 → 商店，添加本商店仓库：
   - Gitee：https://gitee.com/zhqznc_10603234_123/ha-addon
   - GitHub：https://github.com/Treasoni/ha-addon-cn
2. 搜索 silabs-multiprotocol 并安装。

## 配置
| 配置键 | 类型 / 默认值 | 说明 |
| --- | --- | --- |
| `device` | 设备路径（字符串）/ 空 | Silicon Labs 无线模块的串口设备路径 |
| `baudrate` | 枚举（`57600`/`115200`/`230400`/`460800`/`921600`）/ 默认 `460800` | 串口波特率 |
| `flow_control` | 布尔 / `true` | 是否启用串口流控 |
| `autoflash_firmware` | 布尔 / `true` | 启动时是否自动刷写所需的 Multi-PAN 固件 |
| `cpcd_trace` | 布尔 / `false` | 是否输出 CPCD 追踪日志 |
| `otbr_enable` | 布尔 / `true` | 是否启用 OpenThread Border Router 功能 |
| `otbr_log_level` | 枚举（`debug`/`info`/`notice`/`warning`/`error`/`critical`/`alert`/`emergency`）/ 默认 `notice` | OpenThread 边界路由器的日志级别 |
| `otbr_firewall` | 布尔 / `true` | 是否启用防火墙 |
| `network_device` | 字符串 / 空 | 使用的网络设备 |

## 使用 / 访问入口
该加载项没有 Ingress，使用宿主网络运行。端口 9999 用于 EmberZNet EZSP/ASH（供 Zigbee 接入，如 Zigbee2MQTT），端口 8080 为 OpenThread Web 界面，端口 8081 为 OpenThread REST API。

## 常见问题
- **已弃用**：多协议功能不再受支持并将被移除；请将无线模块刷回纯 Zigbee 或 Thread 固件后，改用 ZHA 或 OpenThread Border Router 加载项。
- **固件要求**：无线模块需安装 RCP Multi-PAN 固件才能同时支持多个 802.15.4 PAN；`autoflash_firmware` 会在启动时自动刷写该固件。
- **Zigbee2MQTT 兼容性**：部分 Gecko SDK 版本可能与 Zigbee2MQTT 不兼容，升级前请留意版本说明中的相关警告。

---
- 英文原版：[DEPRECATED] Home Assistant App: SiliconLabs Zigbee/OpenThread Multiprotocol App（[链接](https://github.com/home-assistant/addons/blob/master/silabs-multiprotocol/README.md)）
- 来源仓库：official
