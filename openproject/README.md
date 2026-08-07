<!-- zh-guide -->
# Openproject

## 简介

OpenProject 是一款开源的项目管理与协作平台，支持任务/问题跟踪、甘特图、看板、时间跟踪、文档管理与团队协作等功能，适合家庭或小团队进行项目管理。本加载项基于 OpenProject 官方 Docker 镜像构建，为 Home Assistant 提供开箱即用的项目管理能力。

## 安装

1. 在 Home Assistant → 设置 → 加载项 → 商店，添加本商店仓库：
   - Gitee：https://gitee.com/zhqznc_10603234_123/ha-addon
   - GitHub：https://github.com/Treasoni/ha-addon-cn
2. 搜索 openproject 并安装。

## 配置

启动前请填写默认选项，尤其是 `OPENPROJECT_HOST__NAME` 需要配置为你的 Home Assistant IP 加加载项暴露的端口。可配置选项如下：

| 配置键 | 类型 / 默认值 | 说明 |
| ------ | ------------- | ---- |
| `OPENPROJECT_HOST__NAME` | 字符串，默认 `homeassistant:8080` | OpenProject 的访问主机名，配置为你的 Home Assistant IP 加端口（如 `homeassistant:8080`） |
| `OPENPROJECT_HTTPS` | 布尔，默认 `false` | 是否通过 HTTPS 访问 OpenProject |
| `OPENPROJECT_DEFAULT__LANGUAGE` | 字符串，默认 `en` | OpenProject 的默认界面语言 |
| `OPENPROJECT_SECRET_KEY_BASE` | 字符串（可选） | OpenProject 的加密密钥基础，用于会话与数据加密 |
| `env_vars` | 列表（可选） | 附加环境变量列表，每项包含 `name`（变量名）与 `value`（变量值），用于传入额外的 OpenProject 配置 |

其他高级选项可通过 `env_vars` 传入对应的环境变量，参考上游的 config.yaml 环境变量文档。

## 使用 / 访问入口

启动后打开 Web 界面（端口 `8080/tcp` 映射到宿主端口 `8080`，访问 `http://homeassistant.local:8080`），在界面中完成应用初始化。默认管理员账号为 `admin`，密码为 `admin`，首次登录后请立即修改。修改选项后需要重启加载项才能生效。

## 常见问题

- **无法访问 Web 界面？** 请确认 `OPENPROJECT_HOST__NAME` 已配置为你的 Home Assistant IP 加端口（如 `homeassistant:8080`），并确认宿主端口 `8080` 未被占用。
- **默认管理员账号是什么？** 默认登录为 `admin`，密码为 `admin`，首次登录后务必修改。
- **修改选项后为什么不生效？** OpenProject 的部分选项需要重启加载项才会应用，修改配置后请重启。
- **需要更多配置项怎么办？** 可通过 `env_vars` 选项传入额外的 OpenProject 环境变量（如数据库、邮件等高级配置）。
- **数据保存在哪里？** 加载项数据与附件持久化在 `/config` 与 `/data` 中，升级后会保留。

---
- 英文原版：Home assistant add-on: Openproject；链接 https://github.com/alexbelgium/hassio-addons/blob/master/openproject/README.md
- 来源仓库：alexbelgium
