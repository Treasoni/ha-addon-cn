<!-- zh-guide -->
# Cleanuparr

## 简介

Cleanuparr 自动从你的 \*arr 应用（Sonarr、Radarr、Lidarr、Readarr、Whisparr）与下载客户端（qBittorrent、Deluge、Transmission、NZBGet、SABnzbd）中移除卡住、停滞或不想要的下载，并可通过 Apprise（Discord、Telegram、Slack、邮件等 60+ 渠道）发送通知。

## 安装

1. 在 Home Assistant → 设置 → 加载项 → 商店，添加本商店仓库：
   - Gitee：https://gitee.com/zhqznc_10603234_123/ha-addon
   - GitHub：https://github.com/Treasoni/ha-addon-cn
2. 搜索 `cleanuparr` 并安装。
3. 安装完成后启动 add-on，并查看日志确认运行正常。

## 配置

| 配置键 | 类型 / 默认值 | 说明 |
| --- | --- | --- |
| `env_vars` | 列表 / 空 | 传入容器的额外环境变量（`name`/`value` 形式） |
| `PUID` | 整数 / 默认 `0` | 运行进程的用户 ID |
| `PGID` | 整数 / 默认 `0` | 运行进程的组 ID |
| `TZ` | 字符串 / 默认 `Europe/London` | 时区，如 `Europe/Paris` |

## 使用 / 访问入口

启动后可在 Home Assistant 侧边栏看到 Cleanuparr 图标，点击进入；也可通过 Web 界面端口 11011 直接访问。

## 常见问题

- 持久化配置保存在 HA add-on 配置目录中，可跨 add-on 更新与重装保留。
- 支持监测下载队列并按规则移除停滞或卡住的下载、清理不需要的文件。

---
- 英文原版：[Home Assistant Add-on: Cleanuparr](https://github.com/alexbelgium/hassio-addons/blob/master/cleanuparr/README.md)
- 来源仓库：alexbelgium
