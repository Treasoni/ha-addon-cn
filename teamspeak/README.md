<!-- zh-guide -->
# Teamspeak 服务器

## 简介

TeamSpeak 提供理想的语音通信方案，适用于在线游戏、教育与培训、企业内部沟通以及与亲友保持联系。它专注于易用性、高安全标准、出色的语音质量和低系统与带宽占用。本加载项运行 TeamSpeak 3 服务器，基于 ertagh/teamspeak3-server（ARM）与 mbentley/teamspeak（x64）镜像构建。

## 安装

1. 在 Home Assistant → 设置 → 加载项 → 商店，添加本商店仓库：
   - Gitee：https://gitee.com/zhqznc_10603234_123/ha-addon
   - GitHub：https://github.com/Treasoni/ha-addon-cn
2. 搜索 teamspeak 并安装。

## 配置

修改配置后需要重启加载项才能生效。可选配置键如下：

| 配置键 | 类型/默认值 | 说明 |
| ------ | ----------- | ---- |
| `env_vars` | 列表，默认空 | 传入容器的自定义环境变量列表，每项包含 `name`（变量名，须匹配 `^[A-Za-z0-9_]+$`）与 `value`（变量值，可选）。 |

## 使用 / 访问入口

本加载项没有 Web 界面，它运行一个 TeamSpeak 3 服务器，请使用 TeamSpeak 客户端通过 `homeassistant.local:9987` 连接。相关端口如下：

- 语音通信：`9987/udp`（映射到宿主端口 `9987`）
- ServerQuery（raw）：`10011/tcp`（映射到宿主端口 `10011`）
- 文件传输：`30033/tcp`（映射到宿主端口 `30033`）
- TSDNS：`41144/tcp`（映射到宿主端口 `41144`）

启动后请查看加载项日志，获取 ServerAdmin 密码与特权密钥（ServerAdmin privilege key）。

## 常见问题

- **本加载项没有 Web 界面。** 它只运行 TeamSpeak 3 服务器，需要使用 TeamSpeak 客户端连接访问。
- **如何获取管理员凭据？** 启动并等待初始化完成后，在加载项「日志」中查找 ServerAdmin 密码与 ServerAdmin 特权密钥。
- **外网无法连接？** 需要在路由器上转发上述端口（9987/udp、10011/tcp、30033/tcp、41144/tcp）。
- **如何传入自定义环境变量？** 使用配置中的 `env_vars` 选项，变量名支持大小写，参见上游 wiki「Add environment variables to your add-on」。
- 自 3.13.6-9 版本起新增 `env_vars` 选项用于传入自定义环境变量；从 3.13.6-8 版本起采用新的构建与软件包安装逻辑。
- Home Assistant 项目已弃用 armv7、armhf 与 i386 架构支持，将在 Home Assistant 2025.12 版本中完全移除。

---
- 英文原版：Hass.io Add-ons: Teamspeak；链接 https://github.com/alexbelgium/hassio-addons/blob/master/teamspeak/README.md
- 来源仓库：alexbelgium
