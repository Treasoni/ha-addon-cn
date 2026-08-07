<!-- zh-guide -->
# Silicon Labs Flasher

## 简介
本加载项用于为 Silicon Labs 无线模块刷写固件（Gecko Bootloader 文件格式，`.gbl`）。默认刷写为 Zigbee（Silicon Labs EmberZNet Zigbee 协议栈），并内置了 Home Assistant SkyConnect/ZBT-1 与 Yellow 的固件。

## 安装
1. 在 Home Assistant → 设置 → 加载项 → 商店，添加本商店仓库：
   - Gitee：https://gitee.com/zhqznc_10603234_123/ha-addon
   - GitHub：https://github.com/Treasoni/ha-addon-cn
2. 搜索 silabs_flasher 并安装。

## 配置
| 配置键 | 类型 / 默认值 | 说明 |
| --- | --- | --- |
| `device` | 设备路径（字符串）/ 空 | 要刷写的 Silicon Labs 无线模块的串口设备路径 |
| `bootloader_baudrate` | 枚举（`57600`/`115200`/`230400`/`460800`/`921600`）/ 默认 `115200` | 刷写时使用的波特率 |
| `flow_control` | 布尔 / `true` | 是否启用串口流控 |
| `verbose` | 布尔 / `false` | 是否输出详细日志 |
| `ezsp_baudrate` | 整数 / 空 | 自定义 EZSP 波特率（可选） |
| `firmware_url` | 字符串 / 空 | 自定义固件下载地址（可选） |

## 使用 / 访问入口
该加载项没有 Web 界面，也没有对外端口，属于「运行一次」类型：配置好设备后手动点击「启动」运行一次，刷写完成后会自动停止，结果请查看加载项日志。

## 常见问题
- **刷写前先让出无线模块**：确保没有其他加载项或集成正在使用该无线模块，尤其要停用 Zigbee Home Automation（ZHA）集成和 Silicon Labs Multiprotocol 加载项。
- **默认固件**：默认刷写 EmberZNet Zigbee 固件；可通过 `firmware_url` 指定自定义固件。
- **实验性加载项**：该加载项目前标记为实验性（experimental），请谨慎用于生产环境。

---
- 英文原版：Home Assistant App: Silicon Labs Flasher App（[链接](https://github.com/home-assistant/addons/blob/master/silabs_flasher/README.md)）
- 来源仓库：official
