<!-- zh-guide -->
# deCONZ

## 简介
本加载项基于 dresden elektronik 的 ConBee 或 RaspBee 硬件控制你的 Zigbee 网络。安装并启动后，可在 Home Assistant 中配置 deCONZ 集成，将 Zigbee 设备（灯、开关、传感器等）接入智能家居。

## 安装
1. 在 Home Assistant → 设置 → 加载项 → 商店，添加本商店仓库：
   - Gitee：https://gitee.com/zhqznc_10603234_123/ha-addon
   - GitHub：https://github.com/Treasoni/ha-addon-cn
2. 搜索 deconz 并安装。

## 配置
需要先指定 ConBee/RaspBee 所在的设备路径。设备路径可在 Home Assistant 的「设置 → 系统 → 硬件」页面查看，推荐使用不受其他设备添加影响的 `by-id` 路径。

| 配置键 | 类型 / 默认值 | 说明 |
| --- | --- | --- |
| `device` | 设备路径（字符串）/ 空 | ConBee/RaspBee 的串口设备路径，如 `/dev/serial/by-id/...`、`/dev/ttyUSB0`、`/dev/ttyAMA0` 或 `/dev/ttyACM0`，必填 |
| `ota_update.bosch` | 布尔 / `false` | 是否启用 Bosch 设备的 OTA 固件更新 |
| `ota_update.ikea` | 布尔 / `false` | 是否启用 IKEA 设备的 OTA 固件更新 |
| `ota_update.ledvance` | 布尔 / `false` | 是否启用 OSRAM/LEDVANCE 设备的 OTA 固件更新 |
| `dbg_info` | 整数（0–2）/ 空 | 隐藏选项：deCONZ 信息级调试日志级别，默认 1 |
| `dbg_aps` | 整数（0–2）/ 空 | 隐藏选项：APS 层调试日志级别，默认 0 |
| `dbg_zcl` | 整数（0–1）/ 空 | 隐藏选项：ZCL 层调试日志级别，默认 0 |
| `dbg_zdp` | 整数（0–1）/ 空 | 隐藏选项：ZDP 层调试日志级别，默认 0 |
| `dbg_ddf` | 整数（0–1）/ 空 | 隐藏选项：DDF（设备描述）调试日志级别，默认 0 |
| `dbg_dev` | 整数（0–1）/ 空 | 隐藏选项：设备调试日志级别，默认 0 |
| `dbg_ota` | 整数（0–1）/ 空 | 隐藏选项：OTA 升级调试日志级别，默认 0 |
| `dbg_error` | 整数（0–2）/ 空 | 隐藏选项：错误调试日志级别，默认 0 |
| `dbg_http` | 整数（0–1）/ 空 | 隐藏选项：HTTP 调试日志级别，默认 0 |

## 使用 / 访问入口
启动后可在 Home Assistant 侧边栏看到 deCONZ 图标，点击进入 Web 界面（Phoscon）完成配对设备与配置网关。加载项同时暴露端口 40850（deCONZ API）、端口 8081（WebSocket 界面）与端口 5900（VNC 远程桌面，可查看 Zigbee 网络拓扑），宿主端口为空时由系统自动分配。

## 常见问题
- **Raspberry Pi 上 RaspBee 无法识别**：需要在 SD 卡根目录的 `config.txt` 中添加 `enable_uart=1` 与 `dtoverlay=pi3-miniuart-bt`，再重新启动。
- **默认登录密码**：若 deCONZ 前端没有进入初始设置而一直要求输入密码，可尝试默认密码 `delight`。
- **固件升级**：可在 Phoscon App 中通过「设置 → 网关」直接升级 ConBee/RaspBee 固件；某些 USB 设备（如 Aeotec Z-Wave 棒）可能干扰升级导致静默失败，若升级后版本未变，可拔下其他 USB 设备后重试。
- **电源要求**：建议为 Raspberry Pi 使用至少 2.5A 的电源，避免本加载项运行时的异常行为。
- **迁移数据**：迁移到本加载项前，请先在 Phoscon App 中备份配置，并在安装后恢复，否则灯与分组的名称等数据会丢失（Zigbee 设备仍保持配对状态）。

---
- 英文原版：Home Assistant App: deCONZ（[链接](https://github.com/home-assistant/addons/blob/master/deconz/README.md)）
- 来源仓库：official
