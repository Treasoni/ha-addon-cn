<!-- zh-guide -->
# Signalk Server

## 简介

Signal K Server 是运行在船载中央枢纽上的服务器应用，用于汇聚、处理和分发各类船舶电子设备（AIS、GPS、NMEA0183、CAN 总线等）产生的航行数据。如果你使用或开发船舶电子设备，Signal K Server 都能派上用场。本加载项是 Signal K Server 的实现。

## 安装

1. 在 Home Assistant → 设置 → 加载项 → 商店，添加本商店仓库：
   - Gitee：https://gitee.com/zhqznc_10603234_123/ha-addon
   - GitHub：https://github.com/Treasoni/ha-addon-cn
2. 搜索 `signalk` 并安装。

## 配置

| 配置键 | 类型 / 默认值 | 说明 |
|--------|--------------|------|
| `env_vars` | 列表 / 空 | 传递给 Signal K 的额外环境变量列表（每项含 `name` 和 `value`） |

## 使用 / 访问入口

Web 界面位于宿主端口 3000，SSL Web 界面位于宿主端口 3443，NMEA0183 数据端口为 10110，TCP 数据流端口为 8375。

## 常见问题

- **环境变量**：可通过 `env_vars` 选项传入额外的环境变量（如调整端口等），环境变量名建议使用大写或小写的常见命名。
- **数据接入**：加载项默认将 `/config` 作为 HOME 目录，并已映射 CAN 总线、串口（`/dev/ttyUSB*`、`/dev/ttyACM*`）与 I2C 设备，便于接入各类船舶传感器。
- **网络能力**：加载项带有 NET_ADMIN、NET_RAW 等权限，可在不使用宿主网络的情况下配置 CAN 接口。

---
- 英文原版：[signalk](https://github.com/alexbelgium/hassio-addons/blob/master/signalk/README.md)
- 来源仓库：alexbelgium
