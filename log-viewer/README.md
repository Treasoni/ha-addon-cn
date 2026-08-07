<!-- zh-guide -->
# Log Viewer

## 简介

Log Viewer 是一款基于浏览器的 Home Assistant 日志查看工具。你可以直接在 Web 浏览器中轻松监控 Home Assistant 的运行日志，并通过自定义过滤功能，方便地区分不同类型的日志内容，快速定位问题。

## 安装

1. 在 Home Assistant 中进入「设置 → 加载项 → 商店」，点击右上角菜单添加本商店仓库：
   - Gitee：https://gitee.com/zhqznc_10603234_123/ha-addon
   - GitHub：https://github.com/Treasoni/ha-addon-cn
2. 在商店中搜索 `log-viewer`（Log Viewer）并点击安装。
3. 安装完成后启动加载项，并在日志中确认一切正常。

## 配置

> 注意：修改配置后需重启加载项才会生效。

| 配置键 | 类型 / 默认值 | 说明 |
| --- | --- | --- |
| `log_level` | 枚举（trace\|debug\|info\|notice\|warning\|error\|fatal），可选 / 空 | 控制加载项的日志输出级别。`trace` 显示所有细节；`debug` 显示详细调试信息；`info` 为正常事件；`warning` 为非错误的异常；`error` 为无需立即处理的运行时错误；`fatal` 为致命错误。级别越高包含的日志越少，推荐使用 `info`。 |
| `ssl` | 布尔 / true | 是否在 Log Viewer 上启用 SSL。设为 `true` 启用，`false` 禁用。SSL 仅对直接访问生效，对 Ingress 访问无效。 |
| `certfile` | 字符串 / fullchain.pem | 用于 SSL 的证书文件。文件必须存放在 `/ssl/` 目录下。 |
| `keyfile` | 字符串 / privkey.pem | 用于 SSL 的私钥文件。文件必须存放在 `/ssl/` 目录下。 |
| `leave_front_door_open` | 布尔，可选 / 空 | 设为 `true` 并留空用户名和密码可禁用加载项认证。强烈建议不要启用此选项，即使加载项仅暴露在内网，风险自负。 |

## 使用 / 访问入口

启动后可在 Home Assistant 侧边栏看到 Log Viewer 图标，点击进入即可开始查看日志。

提示：若要查看更多日志，请在 Home Assistant 的 `configuration.yaml` 中启用 `logger` 集成，例如设置 `logger: default: info`。

## 常见问题

- **日志不够详细**：Log Viewer 展示的是 Home Assistant 的日志内容，请确认已启用 `logger` 集成并设置合适的日志级别（如 `info`），否则可能看不到预期的日志。
- **启用了 SSL 却无法通过侧边栏访问**：SSL 设置只作用于直接端口访问，对 Ingress（侧边栏）访问不生效，属正常现象。
- **`leave_front_door_open` 风险提示**：该选项会关闭加载项认证，仅建议在隔离的测试环境使用，生产环境请保持关闭。

---
- 英文原版：Log Viewer；链接 https://github.com/hassio-addons/repository/blob/main/log-viewer/README.md
- 来源仓库：frenck
