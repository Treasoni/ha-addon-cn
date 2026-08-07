<!-- zh-guide -->
# Booksonic air

## 简介

Booksonic air 是一个用于在任意地点访问你自己有声读物的平台。它由 Booksonic Air——一个用于流式播放有声读物的服务器（原 Booksonic 服务器的继任者，基于 Airsonic）——以及基于 DSub 协议的 Booksonic App 组成。本 add-on 基于 linuxserver 的 docker-booksonic-air 镜像。

## 安装

1. 在 Home Assistant → 设置 → 加载项 → 商店，添加本商店仓库：
   - Gitee：https://gitee.com/zhqznc_10603234_123/ha-addon
   - GitHub：https://github.com/Treasoni/ha-addon-cn
2. 搜索 `booksonic_air` 并安装。
3. 安装完成后启动 add-on，点击「保存」并设置你的偏好选项，然后查看日志确认运行正常。

## 配置

| 配置键 | 类型 / 默认值 | 说明 |
| --- | --- | --- |
| `env_vars` | 列表 / 空 | 传入容器的额外环境变量（`name`/`value` 形式） |
| `PGID` | 整数 / 默认 `0` | 文件权限所属组 ID |
| `PUID` | 整数 / 默认 `0` | 文件权限所属用户 ID |
| `TZ` | 字符串（可选） / 空 | 时区，如 `Europe/London` |
| `localdisks` | 字符串（可选） / 空 | 需要挂载的本地磁盘，如 `sda1,sdb1,MYNAS` |
| `networkdisks` | 字符串（可选） / 空 | 需要挂载的 SMB 共享，如 `//SERVER/SHARE` |
| `cifsusername` | 字符串（可选） / 空 | SMB 用户名 |
| `cifspassword` | 字符串（可选） / 空 | SMB 密码 |
| `cifsdomain` | 字符串（可选） / 空 | SMB 域 |

## 使用 / 访问入口

Web 界面可通过 `http://<宿主地址>:4040` 访问（端口 4040）。启动后查看 add-on 日志可获取默认登录凭据。首次使用会进入初始化向导，通过 Web 界面添加你的有声读物目录，并按需配置转码设置。

## 常见问题

- 默认登录凭据显示在启动日志中。
- 首次启动后进入初始化向导，按提示完成配置。
- 通过 Web 界面添加有声读物目录，并配置转码选项。
- 支持挂载本地磁盘与远程 SMB 共享。

---
- 英文原版：[Home assistant add-on: booksonic-air](https://github.com/alexbelgium/hassio-addons/blob/master/booksonic_air/README.md)
- 来源仓库：alexbelgium
