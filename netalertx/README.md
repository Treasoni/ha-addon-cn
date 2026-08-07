<!-- zh-guide -->
# NetAlertX

## 简介

NetAlertX 是一款网络设备存在性与入侵检测工具，提供集中式的网络可见性和持续资产发现能力。它会扫描连接到网络的设备，当发现新的或未知设备时向你发出告警，帮助你及时发现陌生设备接入网络。本加载项基于 jokob-sk 的 NetAlertX 官方 Docker 镜像构建。

## 安装

1. 在 Home Assistant → 设置 → 加载项 → 商店，添加本商店仓库：
   - Gitee：https://gitee.com/zhqznc_10603234_123/ha-addon
   - GitHub：https://github.com/Treasoni/ha-addon-cn
2. 搜索 netalertx 并安装。

## 配置

NetAlertX 的大多数配置（扫描插件、告警规则、通知方式等）都在其 Web 界面中的设置页面完成，无需在此修改。加载项的配置选项如下：

| 配置键 | 类型 / 默认值 | 说明 |
| ------ | ------------- | ---- |
| `TZ` | 字符串（可选） | 容器时区，例如 `Europe/Berlin`，留空使用默认时区 |

首次运行时会自动生成默认的 `app.conf` 与 `app.db` 文件。若界面无法访问，也可以直接修改 `/config/config/app.conf` 文件，但推荐优先使用界面设置。

## 使用 / 访问入口

启动后可在 Home Assistant 侧边栏看到 NetAlertX 图标，点击进入。若需要直接访问，Web 界面端口 `20211/tcp` 映射到宿主端口 `20211`，GraphQL 与 MCP 端口 `20212/tcp` 映射到宿主端口 `20212`。

## 常见问题

- **为什么没有扫描到任何设备？** 必须指定要扫描的网络。如果使用默认的 `ARPSCAN` 插件，需要在 `SCAN_SUBNETS` 设置中至少填写一个从宿主机可达的有效子网和接口，详见上游的 SUBNETS 文档。
- **如何把设备同步到 Home Assistant？** 可通过 NetAlertX 的 MQTT 插件将设备信息同步到 Home Assistant，前提是 Home Assistant 已配置 MQTT 集成。
- **更新后数据目录变化了？** 从某个版本起数据目录改为通过 `/data` 符号链接指向 `/config`，升级前请务必备份安装，以免数据丢失。
- **收到关于 NET_RAW/NET_ADMIN 能力的告警？** 在 Home Assistant Supervisor 下这些能力其实已被授予，但上游审计无法读取到，属于误报，不会影响功能。
- **备份怎么做？** 请按照上游的 Backups 文档备份 `app.conf`、`app.db` 及扫描数据库等数据。

---
- 英文原版：Home assistant add-on: NetAlertX；链接 https://github.com/alexbelgium/hassio-addons/blob/master/netalertx/README.md
- 来源仓库：alexbelgium
