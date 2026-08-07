<!-- zh-guide -->
# Omni Tools

## 简介

Omni Tools 是一个自托管的 Web 应用，汇集了多种日常常用的在线小工具，包括图片缩放与格式转换、视频裁剪、PDF 拆分与合并、文本/列表处理、日期时间计算、数学计算，以及 JSON/CSV/XML 数据处理等。所有文件处理都在浏览器端本地完成，不上传服务器，保障隐私与安全。无广告、无追踪，打开即可使用。

## 安装

1. 在 Home Assistant → 设置 → 加载项 → 商店，添加本商店仓库：
   - Gitee：https://gitee.com/zhqznc_10603234_123/ha-addon
   - GitHub：https://github.com/Treasoni/ha-addon-cn
2. 搜索 omni-tools 并安装。

## 配置

本加载项默认即可直接使用，无需复杂配置。可配置选项如下：

| 配置键 | 类型 / 默认值 | 说明 |
| ------ | ------------- | ---- |
| `env_vars` | 列表（可选） | 附加环境变量列表，每项包含 `name`（变量名）与 `value`（变量值），用于向容器传入额外环境变量 |

## 使用 / 访问入口

打开加载项的 Web 界面（端口 `80/tcp` 映射到宿主端口 `8188`，访问 `http://homeassistant.local:8188`），从各个工具分类中选择所需功能即可使用。所有处理都在浏览器本地完成，隐私安全。

## 常见问题

- **文件会上传到服务器吗？** 不会。所有文件处理都在浏览器端本地进行，不上传任何数据，保障隐私与安全。
- **有哪些工具可用？** 图片工具（缩放、转换）、视频工具（裁剪）、PDF 工具（拆分、合并）、文本/列表工具、日期时间工具、数学工具以及 JSON/CSV/XML 数据处理工具。
- **如何传递自定义环境变量？** 使用 `env_vars` 选项，每项填写 `name` 与 `value`，加载项会将其注入容器环境。
- **需要配置什么吗？** 大多数场景直接启动即可使用，无需额外配置。

---
- 英文原版：Home Assistant Add-on: Omni Tools；链接 https://github.com/alexbelgium/hassio-addons/blob/master/omni-tools/README.md
- 来源仓库：alexbelgium
