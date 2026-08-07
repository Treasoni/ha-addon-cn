<!-- zh-guide -->
# Wger

## 简介

wger Workout Manager 是一款免费、开源的 Web 应用，帮助你管理个人健身训练、体重与饮食计划，也可用作简单的健身房管理工具。它还提供 REST API，便于与其他项目或工具集成。

## 安装

1. 在 Home Assistant → 设置 → 加载项 → 商店，添加本商店仓库：
   - Gitee：https://gitee.com/zhqznc_10603234_123/ha-addon
   - GitHub：https://github.com/Treasoni/ha-addon-cn
2. 搜索 wger 并安装。

## 配置

修改配置后需要重启加载项才能生效。可选配置键如下：

| 配置键 | 类型/默认值 | 说明 |
| ------ | ----------- | ---- |
| `env_vars` | 列表，默认空 | 传入容器的自定义环境变量列表，每项包含 `name`（变量名，须匹配 `^[A-Za-z0-9_]+$`）与 `value`（变量值，可选）。 |
| `CONFIG_LOCATION` | 字符串，默认 `/config/addons_config/wger/config.yaml` | 高级配置使用的 config.yaml 文件位置，可在此文件中以环境变量方式添加更多设置。 |

## 使用 / 访问入口

本加载项不提供 Ingress，通过端口访问：

- Web 界面容器端口 `80/tcp`，宿主端口 9927，访问地址为 `你的HomeAssistant地址:9927`。
- 默认账号：用户名 `admin`，密码 `adminadmin`。**首次登录后请立即修改密码。**

首次启动可能需要等待较长时间（最长约 15 分钟），期间请查看加载项「日志」确认是否正常启动。

## 常见问题

- **启动很慢？** 首次启动（数据库初始化等）最多可能需要 15 分钟，请耐心等待并留意日志中的错误。
- **默认账号密码是什么？** 默认用户名 `admin`、密码 `adminadmin`，登录后请尽快修改。
- **如何配置高级环境变量？** 在 `CONFIG_LOCATION` 指定的 config.yaml 中添加环境变量即可（须为合法 YAML 格式），完整变量列表参见上游文档。
- **需要自定义环境变量？** 通过 `env_vars` 选项传入（变量名支持大小写），参见上游 wiki「Add environment variables to your add-on」。
- 从 2.6-dev-3 起修复了全新安装时 `/data/static` 与 `/data/media` 目录的写权限，确保数据可持久保存；如遇 Web 端口无法访问，可先检查加载项日志中的 nginx 配置错误提示。

---
- 英文原版：Hass.io Add-ons: Wger；链接 https://github.com/alexbelgium/hassio-addons/blob/master/wger/README.md
- 来源仓库：alexbelgium
