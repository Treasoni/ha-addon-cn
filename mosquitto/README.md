<!-- zh-guide -->
# Mosquitto broker

## 简介

Mosquitto broker 是面向 Home Assistant 的开源 MQTT 消息代理（Eclipse Mosquitto）。它基于 MQTT 协议实现，轻量高效，既能运行在树莓派等低功耗单板电脑上，也能胜任完整服务器场景。安装后即可作为 Home Assistant 的 MQTT 服务器使用，官方集成可一键接入。更多信息见 [mosquitto.org](https://mosquitto.org)。

## 安装

1. 在 Home Assistant → 设置 → 加载项 → 商店，添加本商店仓库：
   - Gitee：https://gitee.com/zhqznc_10603234_123/homeassistant
   - GitHub：https://github.com/Treasoni/ha-addon-cn
2. 搜索 mosquitto 并安装。

## 配置

| 配置键 | 类型 / 默认值 | 说明 |
| --- | --- | --- |
| `logins` | 数组，默认空 | 本地用户列表，每项包含 `username`、`password`，可选用预哈希密码 `password_pre_hashed: true`。一般无需配置，直接用 Home Assistant 用户即可 |
| `log_dest` | 数组，默认空（实际默认 `stdout`） | 日志输出目标，可选 `none` / `stdout` / `stderr` / `topic`。不支持 `file` |
| `log_type` | 数组，默认空（实际默认 `error`、`warning`、`notice`、`information`） | 日志类型，可选 `none` / `debug` / `error` / `warning` / `notice` / `information` / `subscribe` / `unsubscribe` / `websockets` / `all`；开启 `debug` 时本项被忽略，改用 `log_type all` |
| `require_certificate` | 布尔，默认 `false` | 是否强制客户端提供证书连接。为 `false` 时用户名密码即可，且忽略 `cafile`；为 `true` 时客户端必须提供由 `cafile` 签发的证书 |
| `certfile` | 字符串，默认 `fullchain.pem` | 服务器证书（含证书链），需放在 Home Assistant 的 `ssl` 目录 |
| `keyfile` | 字符串，默认 `privkey.pem` | 服务器私钥，需放在 Home Assistant 的 `ssl` 目录 |
| `cafile` | 字符串，可选 | 根证书文件，需放在 Home Assistant 的 `ssl` 目录 |
| `customize.active` | 布尔，默认 `false` | 为 `true` 时读取额外的自定义配置文件 |
| `customize.folder` | 字符串，默认 `mosquitto` | 存放额外配置 `*.conf` 的目录（对应 `/share/` 下） |
| `debug` | 布尔，可选 | 为 `true` 时开启 mosquitto 及其认证插件的调试日志，便于排查问题；长时间开启会记录敏感信息，不建议长期使用 |

## 使用 / 访问入口

加载项提供 4 个监听端口（无 Web 管理界面 / ingress）：

- `1883`：明文 MQTT
- `1884`：明文 WebSocket
- `8883`：TLS 加密 MQTT（需配置 `certfile`/`keyfile` 后启用）
- `8884`：TLS 加密 WebSocket（需配置 `certfile`/`keyfile` 后启用）

首次使用步骤：

1. 启动加载项并等待片刻，查看日志确认运行正常。
2. 在 Home Assistant 前端 **设置 → 人员 → 用户** 中创建 MQTT 用户（不是加载项配置页里创建）。用户名不能是保留的 `homeassistant` 或 `addons`；若看不到创建用户的入口，请先在个人资料中开启「高级模式」。
3. 在 **设置 → 设备与服务 → 集成** 页面，顶部会显示被发现的 MQTT 集成，选中并提交即可一键接入；如需可勾选启用 MQTT 发现。已有旧的 MQTT 集成请先删除并重启 Home Assistant。

如需限制对主题的访问，可开启 `customize.active`，在 `/share/mosquitto/` 下配置 ACL 文件（该目录可通过 SMB 或主机 `/usr/share/hassio/share` 访问）。注意：本加载项不支持匿名登录，所有连接都必须使用用户名和密码。

## 常见问题

- **连接报「认证失败 / 拒绝访问」？** 本加载项不支持匿名登录，请确认客户端使用了在 Home Assistant「人员 → 用户」中创建的账号密码连接。
- **如何启用加密连接？** 在 `ssl` 目录放置证书与私钥并填写 `certfile`/`keyfile`，即可在 `8883`/`8884` 端口提供 TLS 加密的 MQTT / WebSocket 服务，客户端需信任服务器证书。
- **如何禁用不安全的 `1883`/`1884` 端口？** 在加载项页面的「网络」卡片中把这两个端口设为空白即可关闭。
- **如何限制特定用户访问某些主题？** 开启 `customize.active`，参考 DOCS 中 ACL 示例在 `/share/mosquitto/` 下创建 `acl.conf` 与访问控制列表，并保证 `homeassistant`、`addons` 用户拥有全主题读写权限。

---
- 英文原版：Home Assistant App: Mosquitto broker；链接 https://github.com/home-assistant/addons/blob/master/mosquitto/README.md
- 来源仓库：official
