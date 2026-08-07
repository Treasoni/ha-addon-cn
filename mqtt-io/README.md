<!-- zh-guide -->
# MQTT IO

## 简介

MQTT IO 通过 MQTT 协议把通用输入输出（GPIO）、硬件传感器和串口设备暴露出来，供远程控制与监控使用。非常适合 Raspberry Pi 等单板计算机，让你能把底层的引脚、传感器和串行设备方便地接入 Home Assistant 的 MQTT 生态。

## 安装

1. 在 Home Assistant 中进入「设置 → 加载项 → 商店」，点击右上角菜单添加本商店仓库：
   - Gitee：https://gitee.com/zhqznc_10603234_123/ha-addon
   - GitHub：https://github.com/Treasoni/ha-addon-cn
2. 在商店中搜索 `mqtt-io`（MQTT IO）并点击安装。
3. 在加载项配置中设置 MQTT IO 配置文件的位置（默认为 `/config/mqtt-io/config.yml`）。
4. 手动创建 MQTT IO 配置文件。该文件不会自动生成，其格式与配置选项请参考 MQTT IO 官方文档：<https://mqtt-io.app/#/config/scenarios>
5. 配置文件就绪后启动加载项，并在日志中确认一切正常。

## 配置

> 注意：修改配置后需重启加载项才会生效。

| 配置键 | 类型 / 默认值 | 说明 |
| --- | --- | --- |
| `configuration_file` | 字符串 / /config/mqtt-io/config.yml | MQTT IO 运行时使用的配置文件路径。可按需修改，但该文件不会自动创建，需自行编写。配置文件格式与 HA 发现配置参考 MQTT IO 官方文档。 |
| `log_level` | 枚举（trace\|debug\|info\|notice\|warning\|error\|fatal），可选 / 空 | 加载项的日志输出级别。`trace` 显示全部细节，`debug` 显示详细调试信息，`info` 为正常事件，`warning` 为非错误的异常，`error` 为无需立即处理的错误，`fatal` 为致命错误。推荐使用 `info`。 |

## 使用 / 访问入口

MQTT IO 不提供 Web 界面，也不会开放端口。它通过读取配置文件，将 GPIO、传感器和串口设备以 MQTT 主题的形式暴露给 MQTT 服务器，Home Assistant 可通过 MQTT 集成发现并控制这些设备。配置文件就绪并启动后，可在 Home Assistant 的 MQTT 中发现设备。

## 常见问题

- **加载项无法启动 / 设备不出现**：MQTT IO 依赖手动创建的配置文件（默认 `/config/mqtt-io/config.yml`），该文件不会自动生成。请先按官方文档创建配置文件，再启动加载项。
- **修改配置文件不生效**：修改后请重启加载项，使新配置生效。
- **日志过少**：可临时将 `log_level` 调为 `debug` 或 `trace` 排查问题，确认后改回 `info`。
- **适用架构**：本加载项支持 aarch64、amd64、armv7，已停止对 armhf 与 i386 的支持。

---
- 英文原版：MQTT IO；链接 https://github.com/hassio-addons/repository/blob/main/mqtt-io/README.md
- 来源仓库：frenck
