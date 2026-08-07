<!-- zh-guide -->
# EMQX

## 简介

EMQX 是一款面向物联网（IoT）场景、极具可扩展性的开源 MQTT 消息代理，可作为 Home Assistant 中 Mosquitto 加载项的替代方案。它提供可视化 Web 界面，方便进行认证、ACL 权限、监听器等各项配置，适合对 MQTT 功能有更高要求的用户。

## 安装

1. 在 Home Assistant → 设置 → 加载项 → 商店，添加本商店仓库：
   - Gitee：https://gitee.com/zhqznc_10603234_123/ha-addon
   - GitHub：https://github.com/Treasoni/ha-addon-cn
2. 搜索 emqx 并安装。

## 配置

大部分配置都可以通过加载项提供的 Web 界面完成，无需修改配置项；只有 Web 界面未覆盖的高级配置（例如搭建多实例集群）才需要在这里设置。修改配置后需要重启加载项才能生效。可选配置键如下：

| 配置键 | 类型/默认值 | 说明 |
| ------ | ----------- | ---- |
| `env_vars` | 列表/对象列表（含 `name`、`value` 子键），默认 `空` | 通过环境变量调整 EMQX 的任意配置。仅接受以 `EMQX_` 开头的环境变量，子键 `name` 为变量名、`value` 为变量值；变量用法详见 EMQX 官方配置文档 |

## 使用 / 访问入口

- **Web 界面**：加载项支持 Ingress，启动后可在 Home Assistant 侧边栏看到 EMQX 图标，点击进入。默认登录账号为 `admin`，密码为 `public`。
- **重要：配置认证**：首次使用请务必在 EMQX Web 界面的“访问控制”（Access Control）→“认证”（Authentication）中为 MQTT 客户端配置认证方式，否则存在安全风险。
- **客户端连接地址**：Home Assistant 本机上的 MQTT 客户端（如 Zigbee2MQTT）可将 `homeassistant` 或 `a0d7b954-emqx` 作为 broker 主机名连接；外部设备连接时，请使用 Home Assistant 实例的 IP 地址或主机名。

## 常见问题

- **能与 Mosquitto 加载项同时运行吗？** 不能。本加载项与 Mosquitto 加载项无法同时运行。
- **端口冲突怎么办？** EMQX 默认使用端口 1883、8083、8084 和 8883，可能与现有加载项冲突。此时可通过 EMQX Web 界面修改监听端口（修改前需临时停止冲突的加载项）。
- **WebRTC 集成导致端口冲突？** AlexxIT 的 WebRTC 集成已知会在端口 8083 上造成冲突，可临时禁用该集成以进入 EMQX Web 界面调整监听器。
- **如何重置默认密码？** 请在 Web 界面中通过“访问控制”为 MQTT 客户端创建独立的认证用户，并修改管理员账号的密码。

---
- 英文原版：Home Assistant Community Add-on: EMQX；链接 https://github.com/hassio-addons/repository/blob/main/emqx/README.md
- 来源仓库：frenck
