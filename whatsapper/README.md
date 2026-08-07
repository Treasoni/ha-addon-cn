<!-- zh-guide -->
# Whatsapper

## 简介

Whatsapper 是用于 Home Assistant 的 WhatsApp 工具，提供多种调整与配置选项，可让你在 Home Assistant 中收发 WhatsApp 消息。本加载项基于 whatsapper/whatsapper 镜像构建，使用前需配合 HACS 集成 whatsapper-ha-integration（https://github.com/baldarn/whatsapper-ha-integration）一起使用。

## 安装

1. 在 Home Assistant → 设置 → 加载项 → 商店，添加本商店仓库：
   - Gitee：https://gitee.com/zhqznc_10603234_123/ha-addon
   - GitHub：https://github.com/Treasoni/ha-addon-cn
2. 搜索 whatsapper 并安装。
3. 在 HACS 中安装 whatsapper-ha-integration 集成，并按其中的说明完成系统配置。

## 配置

修改配置后需要重启加载项才能生效。可选配置键如下：

| 配置键 | 类型/默认值 | 说明 |
| ------ | ----------- | ---- |
| `env_vars` | 列表，默认空 | 传入容器的自定义环境变量列表，每项包含 `name`（变量名，须匹配 `^[A-Za-z0-9_]+$`）与 `value`（变量值，可选）。 |

## 使用 / 访问入口

本加载项不提供 Ingress，通过端口访问：

- Web 界面/API 容器端口 `3000/tcp`，宿主端口 4000，访问地址为 `你的HomeAssistant地址:4000`。

首次使用：启动加载项并打开 Web 界面完成应用初始化，然后**重启加载项**以应用相关选项。

## 常见问题

- **如何在 Home Assistant 中使用？** 需要先在 HACS 中安装 whatsapper-ha-integration 集成，并按照该集成仓库的说明配置后才能使用。
- **初始化后如何生效？** 在 Web 界面完成初始化后，重启加载项即可应用选项。
- **需要自定义环境变量？** 通过 `env_vars` 选项传入（变量名支持大小写），参见上游 wiki「Add environment variables to your add-on」。
- 从 1.0.5 版本起新增 `env_vars` 选项；从 2024.4.29 起修复了 whatsapp-web.js 客户端问题，请保持加载项为最新版本以获得稳定的连接。

---
- 英文原版：Home assistant add-on: Whatsapper；链接 https://github.com/alexbelgium/hassio-addons/blob/master/whatsapper/README.md
- 来源仓库：alexbelgium
