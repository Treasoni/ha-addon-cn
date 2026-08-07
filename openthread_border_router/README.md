<!-- zh-guide -->
# OpenThread Border Router

## 简介
本加载项将上游 OpenThread Border Router 实现打包为 Home Assistant 应用，用于组建或加入 Thread 网络，让 Home Assistant 成为 Thread Border Router，从而为 Matter over Thread 设备提供边界路由。

## 安装
1. 在 Home Assistant → 设置 → 加载项 → 商店，添加本商店仓库：
   - Gitee：https://gitee.com/zhqznc_10603234_123/ha-addon
   - GitHub：https://github.com/Treasoni/ha-addon-cn
2. 搜索 openthread_border_router 并安装。

## 配置
| 配置键 | 类型 / 默认值 | 说明 |
| --- | --- | --- |
| `device` | 设备路径（字符串）/ 空 | 802.15.4 无线模块的串口设备路径（必填）；使用 Home Assistant Yellow 或 Connect ZBT-1 时固件会自动安装 |
| `baudrate` | 枚举（`57600`/`115200`/`230400`/`460800`/`921600`/`1000000`）/ 默认 `460800` | 串口波特率 |
| `flow_control` | 布尔 / `true` | 是否启用串口流控 |
| `otbr_log_level` | 枚举（`debug`/`info`/`notice`/`warning`/`error`/`critical`/`alert`/`emergency`）/ 默认 `notice` | OpenThread 边界路由器的日志级别 |
| `firewall` | 布尔 / `true` | 是否启用防火墙 |
| `nat64` | 布尔 / `false` | 是否启用 NAT64（在 IPv6 网络与 IPv4 之间转换流量） |
| `beta` | 布尔 / `false` | 是否使用 beta 版本 |
| `backbone_interface` | 字符串 / 空 | 覆盖用于 IPv6 路由的网络接口 |
| `network_device` | 字符串 / 空 | 使用的网络设备 |

## 使用 / 访问入口
该加载项没有 Ingress，使用宿主网络运行。启动后可通过端口 8080 访问 OpenThread Web 界面，端口 8081 为 OpenThread REST API。

## 常见问题
- **硬件要求**：需要一个支持 802.15.4 且带有 OpenThread RCP 固件的无线模块。如果使用 Home Assistant Yellow 或 Connect ZBT-1（原 SkyConnect），正确的固件会自动安装。
- **Thread 1.4**：自 v3.0.0 起 Thread 1.4 为稳定版本，OpenThread 内置的 mDNS 成为默认；如需继续运行 beta，请手动开启 `beta` 选项。
- **IPv6 路由**：若未启用 IPv6 路由，加载项会打印警告；也可用 `backbone_interface` 覆盖用于 IPv6 路由的网络接口。
- **NAT64 与安全**：`nat64` 仅在必要且网络可信时启用。

---
- 英文原版：Home Assistant App: OpenThread Border Router App（[链接](https://github.com/home-assistant/addons/blob/master/openthread_border_router/README.md)）
- 来源仓库：official
