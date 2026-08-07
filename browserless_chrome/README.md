<!-- zh-guide -->
# Browserless Chromium

## 简介

Browserless Chromium 是一种将 Chromium 作为服务运行的容器化方案，允许远程客户端连接、驱动并执行无头（headless）工作。本 add-on 基于 browserless/chrome 镜像，为需要无头浏览器的自动化任务提供服务。

## 安装

1. 在 Home Assistant → 设置 → 加载项 → 商店，添加本商店仓库：
   - Gitee：https://gitee.com/zhqznc_10603234_123/ha-addon
   - GitHub：https://github.com/Treasoni/ha-addon-cn
2. 搜索 `browserless_chrome` 并安装。
3. 安装完成后启动 add-on，点击「保存」并设置你的偏好选项，然后查看日志确认运行正常。

## 配置

| 配置键 | 类型 / 默认值 | 说明 |
| --- | --- | --- |
| `env_vars` | 列表 / 空 | 传入容器的额外环境变量（`name`/`value` 形式） |
| `TIMEOUT` | 整数 / 默认 `60000` | 请求超时时间（毫秒） |

## 使用 / 访问入口

Web 界面可通过 `http://<宿主地址>:3000` 访问（端口 3000），默认 API 文档位于 `/docs`。除上述选项外，其余配置可在应用的 Web 界面中完成。

## 常见问题

- 大部分配置可通过应用 Web 界面完成，仅 `TIMEOUT` 等少量选项需要在 add-on 选项中设置。
- 可通过 `env_vars` 选项传入额外环境变量，或通过 addon_config 映射运行自定义脚本。

---
- 英文原版：[Home assistant add-on: Browserless Chrome](https://github.com/alexbelgium/hassio-addons/blob/master/browserless_chrome/README.md)
- 来源仓库：alexbelgium
