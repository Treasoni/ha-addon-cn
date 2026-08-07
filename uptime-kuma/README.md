<!-- zh-guide -->
# Uptime Kuma

## 简介
Uptime Kuma 是一款开源的自托管监控工具，可类比于商业服务 "Uptime Robot" 的自托管版本。它支持通过 HTTP/S、TCP、DNS 等多种协议监控服务，并能在服务宕机时发送通知，或触发 Home Assistant 自动化 Webhook。

## 安装
1. 在 Home Assistant → 设置 → 加载项 → 商店，添加本商店仓库：
   - Gitee：https://gitee.com/zhqznc_10603234_123/homeassistant
   - GitHub：https://github.com/Treasoni/ha-addon-cn
2. 搜索 uptime-kuma 并安装。

## 配置
本加载项**没有配置选项**（config.yaml 中不含 `options`/`schema`）。所有功能都直接在 Uptime Kuma 的 Web 界面中管理和配置。

以下几点值得了解：

| 特性 | 说明 |
|------|------|
| Home Assistant 发现 | 加载项会向 Home Assistant 广播自身，使 Uptime Kuma 集成可被自动发现并配置 |
| 数据持久化 | 所有监控项、设置与历史数据存放在加载项的 `/data` 目录，重启与更新后依然保留，并会纳入 Home Assistant 备份 |
| 通知 | 内置 Apprise 与 MQTT，可在 Uptime Kuma 界面中直接配置对应的通知渠道 |
| Cloudflare Tunnel | 内置 `cloudflared` 客户端，可使用 Uptime Kuma 自带的 Cloudflare Tunnel 功能，无需暴露端口即可安全远程访问 |

## 使用 / 访问入口
- 安装并启动加载项后，点击 "OPEN WEB UI"（打开 Web UI）按钮即可进入 Uptime Kuma 界面。
- Web 界面默认监听端口：**3001**。
- 首次访问时，在 Uptime Kuma 界面中创建管理员账号并开始添加监控项。

## 常见问题
- **数据会丢吗？** 不会。监控项、设置与历史数据都保存在 `/data` 目录，升级或重启后依然保留，并包含在 Home Assistant 备份中。
- **如何远程安全访问？** 可使用内置的 Cloudflare Tunnel 功能，无需在路由器上开放端口。
- **如何接收宕机通知？** 加载项内置 Apprise 与 MQTT，可在 Uptime Kuma 的通知设置中直接配置通知渠道。

---
- 英文原版：Home Assistant Community App: Uptime Kuma；链接 https://github.com/hassio-addons/repository/blob/master/uptime-kuma/README.md
- 来源仓库：frenck
