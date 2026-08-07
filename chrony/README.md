<!-- zh-guide -->
# chrony

## 简介

chrony 是一个 NTP（网络时间协议）时间服务器加载项，可让本地网络上的所有设备（如摄像头等无法访问外网的设备）同步时间。

## 安装

1. 在 Home Assistant → 设置 → 加载项 → 商店，添加本商店仓库：
   - Gitee：https://gitee.com/zhqznc_10603234_123/ha-addon
   - GitHub：https://github.com/Treasoni/ha-addon-cn
2. 搜索 chrony 并安装。
3. 保存配置并启动加载项。本加载项使用 `system` 启动模式，启动时同步系统时钟。

## 配置

所有配置项均可在加载项的「配置」页面编辑，保存并重启后生效。

| 配置键 | 类型 / 默认值 | 说明 |
|--------|--------------|------|
| `set_system_clock` | 布尔 / `true` | 是否把系统时钟设为 NTP 同步的时间 |
| `mode` | 枚举 / `pool` | 时间来源模式：`pool`（使用时间池）或 `server`（使用指定服务器） |
| `ntp_pool` | 字符串 / `pool.ntp.org` | `mode` 为 `pool` 时使用的时间池地址 |
| `ntp_server` | 字符串列表 / `54.39.13.155, briareus.schulte.org` | `mode` 为 `server` 时使用的 NTP 服务器地址列表 |
| `log_level` | 枚举 / 空 | 日志级别：`trace`/`debug`/`info`/`notice`/`warning`/`error`/`fatal`，留空使用默认级别 |

## 使用 / 访问入口

本加载项为后台服务，没有 Web 界面。启动后在本机监听 NTP 端口 `123/udp`，局域网内的设备可将 NTP 服务器指向 Home Assistant 的 IP 来同步时间（如摄像头、NAS 等）。

## 常见问题

- **设备无法同步时间**：确认设备与 Home Assistant 在同一局域网，NTP 服务器地址填写 HA 主机 IP（默认端口 `123/udp`）。
- **摄像头等受限设备**：chrony 主要面向无法直接访问外网时间的设备，请把它们的 NTP 指向本加载项。

---
- 英文原版：Home Assistant Community Add-on: chrony；链接 https://github.com/hassio-addons/addon-chrony
- 来源仓库：frenck
