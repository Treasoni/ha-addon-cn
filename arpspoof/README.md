<!-- zh-guide -->
# Arpspoof

## 简介

Arpspoof 可以切断局域网内指定设备的互联网连接，用于家长控制、临时断网等场景。它基于 [Arpspoof-Docker](https://github.com/t0mer/Arpspoof-Docker) 镜像（hub.docker.com/r/techblog/arpspoof-docker）实现，通过 ARP 欺骗对目标设备实施断网，并提供 Web 界面进行控制。

## 安装

1. 在 Home Assistant → 设置 → 加载项 → 商店，添加本商店仓库：
   - Gitee：https://gitee.com/zhqznc_10603234_123/ha-addon
   - GitHub：https://github.com/Treasoni/ha-addon-cn
2. 搜索 arpspoof 并安装。
3. 保存配置并启动加载项，然后打开 Web 界面调整软件选项。

## 配置

该加载项使用宿主网络（host_network），必须正确填写 `ROUTER_IP`。配置键如下：

| 配置键 | 类型 / 默认值 | 说明 |
| ------ | ----------- | ---- |
| `ROUTER_IP` | 字符串，默认 `yourip` | 路由器 IP 地址（必填），用于确定要欺骗的网关 |
| `INTERFACE_NAME` | 可选字符串，默认空 | 网卡接口名称；留空时会自动填充 |
| `env_vars` | 列表，默认空 | 附加环境变量，通过此选项传入额外的环境变量（变量名大小写均可） |

## 使用 / 访问入口

- **Web 界面**：启动后可通过 Web 界面管理，地址为 http://homeassistant:7022（容器端口 `7022/tcp` 映射到宿主端口 `7022`）。
- **在 Home Assistant 中使用**：可添加 `command_line` 开关临时断开局域网内某设备的网络，例如 `command_off` 调用 `http://{HA-IP}:7022/disconnect?ip={iPhoneIP}`、`command_on` 调用 `http://{HA-IP}:7022/reconnect?ip={iPhoneIP}`，并配合 `command_state`/`value_template` 读取 `http://{HA-IP}:7022/status?ip={iPhoneIP}` 返回状态（`1` 表示已断开）。

## 常见问题

- **无法断网？** 请确认 `ROUTER_IP` 已填成你真实的网关 IP，且加载项运行在宿主网络模式下，能访问到同一局域网。
- **`INTERFACE_NAME` 要填吗？** 可选，留空时加载项会自动填充。
- **如何临时恢复设备联网？** 调用 `http://{HA-IP}:7022/reconnect?ip={设备IP}` 即可重新连接；请确保端口 `7022` 在宿主机上可访问。

---
- 英文原版：Home assistant add-on: Arpspoof；链接 https://github.com/alexbelgium/hassio-addons/blob/master/arpspoof/README.md
- 来源仓库：alexbelgium
