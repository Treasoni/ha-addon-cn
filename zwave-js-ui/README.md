<!-- zh-guide -->
# Z-Wave JS UI

## 简介

Z-Wave JS UI 是一个功能完备、可深度配置的 Z-Wave JS 控制面板与 MQTT 网关。它提供一个解耦的网关，可同时通过 Z-Wave JS WebSocket（Home Assistant Z-Wave JS 集成所用）和 MQTT 通信，让你配置 Z-Wave 网络的每一个方面。它与 Home Assistant Z-Wave JS 集成兼容，Home Assistant 重启时 Z-Wave 网络不会中断，也支持 Node-RED、ESPHome 等直接使用你的 Z-Wave 网络；发现 Mosquitto 应用时会自动完成预配置。

## 安装

1. 在 Home Assistant → 设置 → 加载项 → 商店，添加本商店仓库：
   - Gitee：https://gitee.com/zhqznc_10603234_123/ha-addon
   - GitHub：https://github.com/Treasoni/ha-addon-cn
2. 搜索 zwave-js-ui 并安装。

## 配置

本应用无需在加载项配置页面填写选项，所有设置均在 Z-Wave JS UI 控制面板中完成。首次使用请进入控制面板的「Settings → Zwave」，填入 Z-Wave 控制器的串口路径（例如 `/dev/serial/by-id/...`）与安全网络密钥（Network Key），保存后即可开始管理设备。

## 使用 / 访问入口

启动后可在 Home Assistant 侧边栏看到 **Z-Wave JS** 图标（面板标题为 Z-Wave JS），点击进入 Z-Wave JS UI 控制面板，可查看节点、配对/移除设备、查看网络拓扑、调整配置参数与升级固件等。

## 常见问题

1. **如何让 Home Assistant 使用本应用的 Z-Wave 网络**：进入 设置 → 设备与服务 → 添加集成 → 选择「Z-Wave」，在弹出的对话框中 **取消勾选**「使用 Z-Wave JS Supervisor 应用」（即不安装 HA 自带的 Z-Wave JS 应用），在服务器地址填入 `ws://a0d7b954-zwavejs2mqtt:3000`，确认即可完成连接。
2. **不要使用 MQTT 发现功能接入 Home Assistant**：Z-Wave JS UI 支持通过 MQTT 发现接入 Home Assistant，但强烈建议不要使用该方式，而应使用上面的 Z-Wave JS 集成方式。
3. **网络在 Home Assistant 重启之间持续运行**：Z-Wave 网络由本应用独立管理，重启 Home Assistant 不会中断 Z-Wave 设备的连接。
4. **Mosquitto 自动预配置**：若检测到 Mosquitto 应用，本应用会自动预配置与它的 MQTT 连接，方便 Node-RED、ESPHome 等直接使用 Z-Wave 网络。

---
- 英文原版：[Home Assistant Community App: Z-Wave JS UI](https://github.com/hassio-addons/repository/blob/main/zwave-js-ui/README.md)
- 来源仓库：frenck
