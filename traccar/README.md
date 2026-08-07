<!-- zh-guide -->
# Traccar

## 简介

Traccar 是一款现代 GPS 追踪平台。本加载项让你无需任何云端服务，即可在 Home Assistant 中运行自己的 GPS 追踪软件。Traccar 支持的协议与设备型号比市面上其他 GPS 追踪系统都多，从低成本的国产追踪器到高端品牌均可选择。

Traccar 还提供 Android 和 iOS 原生 App，可追踪你的手机等设备。同时，通过 Home Assistant 的 `traccar` 集成，Traccar 中的数据也能回传到你的 Home Assistant 实例中。

## 安装

1. 在 Home Assistant 中进入「设置 → 加载项 → 商店」，点击右上角菜单添加本商店仓库：
   - Gitee：https://gitee.com/zhqznc_10603234_123/ha-addon
   - GitHub：https://github.com/Treasoni/ha-addon-cn
2. 在商店中搜索 `traccar`（Traccar）并点击安装。
3. 启动加载项并在日志中确认一切正常，然后打开 Web 界面。

## 配置

> 注意：修改配置后需重启加载项才会生效。

| 配置键 | 类型 / 默认值 | 说明 |
| --- | --- | --- |
| `log_level` | 枚举（trace\|debug\|info\|notice\|warning\|error\|fatal），可选 / 空 | 加载项的日志输出级别。`trace` 显示全部细节，`debug` 显示详细调试信息，`info` 为正常事件，`warning` 为非错误的异常，`error` 为无需立即处理的错误，`fatal` 为致命错误。推荐使用 `info`。 |
| `ssl` | 布尔 / false | 是否在 Web 界面上启用 SSL（HTTPS）。设为 `true` 启用，`false` 禁用。 |
| `certfile` | 字符串 / fullchain.pem | 用于 SSL 的证书文件，必须存放在 `/ssl/` 目录下。 |
| `keyfile` | 字符串 / privkey.pem | 用于 SSL 的私钥文件，必须存放在 `/ssl/` 目录下。 |

## 使用 / 访问入口

本加载项不提供 Ingress 入口，通过端口访问。容器端口 `80/tcp`（Web 界面）的宿主映射为 8082，在浏览器中打开 `你的HA地址:8082` 即可访问（即通过端口 8082 访问；若启用了 `ssl`，请使用 HTTPS 协议）。

## 常见问题

- **启用更多协议**：为减少开放端口，默认仅启用 OsmAnd 协议（Traccar App 使用）与 API。如需更多协议，可在加载项配置文件夹的 `traccar.xml` 中添加相应条目。
- **与 Home Assistant 集成**：可添加 Home Assistant 的 `traccar` 集成，把 Traccar 中的设备数据回传到 Home Assistant。
- **启用 SSL 后访问方式**：启用 `ssl` 后请使用 HTTPS 协议访问界面，证书与私钥需放在 `/ssl/` 目录。
- **移动端追踪**：可安装 Traccar 官方 Android/iOS App 来追踪设备。

---
- 英文原版：Traccar；链接 https://github.com/hassio-addons/repository/blob/main/traccar/README.md
- 来源仓库：frenck
