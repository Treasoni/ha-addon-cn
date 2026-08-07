<!-- zh-guide -->
# TasmoAdmin

## 简介

TasmoAdmin（原名 SonWEB）是一个集中管理所有 Sonoff-Tasmota 设备的 Web 管理界面。主要功能：

- 自动扫描你的网络并添加设备。
- 快速方便地查看所有设备状态。
- 从单一界面集中配置所有设备。
- 一次向一台或多台设备推送 OTA 固件更新。
- 自动为你下载最新固件。

## 安装

1. 在 Home Assistant 中进入「设置 → 加载项 → 商店」，点击右上角菜单添加本商店仓库：
   - Gitee：https://gitee.com/zhqznc_10603234_123/ha-addon
   - GitHub：https://github.com/Treasoni/ha-addon-cn
2. 在商店中搜索 `tasmoadmin`（TasmoAdmin）并点击安装。
3. 启动加载项并在日志中确认一切正常，然后打开 Web 界面。

## 配置

> 注意：修改配置后需重启加载项才会生效。

| 配置键 | 类型 / 默认值 | 说明 |
| --- | --- | --- |
| `log_level` | 枚举（trace\|debug\|info\|notice\|warning\|error\|fatal），可选 / 空 | 加载项的日志输出级别。`trace` 显示全部细节，`debug` 显示详细调试信息，`info` 为正常事件，`warning` 为非错误的异常，`error` 为无需立即处理的错误，`fatal` 为致命错误。推荐使用 `info`。 |
| `ssl` | 布尔 / true | 是否在 TasmoAdmin 面板的 Web 界面上启用 SSL（HTTPS）。设为 `true` 启用，`false` 禁用。注意：Tasmota 设备不支持通过 SSL 进行 OTA 更新。 |
| `certfile` | 字符串 / fullchain.pem | 用于 SSL 的证书文件，必须存放在 `/ssl/` 目录下。 |
| `keyfile` | 字符串 / privkey.pem | 用于 SSL 的私钥文件，必须存放在 `/ssl/` 目录下。 |

## 使用 / 访问入口

本加载项不提供 Ingress 入口，通过端口访问：在浏览器中打开 `你的Home Assistant地址:9541`（若启用了 `ssl`，则使用 `https` 协议）。端口 `9541/tcp` 为 TasmoAdmin 的 Web 界面端口，宿主端口映射为 `9541`。

## 常见问题

- **OTA 更新失败**：Tasmota 设备不支持通过 SSL 进行 OTA，请在使用 OTA 固件更新前临时关闭 `ssl`，或确保设备与界面之间使用非 HTTPS 访问。
- **设备无法自动发现**：请确认设备与 Home Assistant 处于同一网络，可手动添加设备。
- **启用 SSL 后访问方式**：启用 `ssl` 后请使用 HTTPS 协议访问界面，证书与私钥需放在 `/ssl/` 目录。
- **适用架构**：本加载项支持 aarch64、amd64，已停止对 armv7 的支持。

---
- 英文原版：TasmoAdmin；链接 https://github.com/hassio-addons/repository/blob/main/tasmoadmin/README.md
- 来源仓库：frenck
