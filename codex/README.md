<!-- zh-guide -->
# Codex

## 简介

Codex 是一个基于 Web 的漫画压缩包浏览与阅读器。本 add-on 基于 ajslater 的官方 codex 镜像，让你在 Home Assistant 中通过浏览器浏览和阅读漫画压缩包。

## 安装

1. 在 Home Assistant → 设置 → 加载项 → 商店，添加本商店仓库：
   - Gitee：https://gitee.com/zhqznc_10603234_123/ha-addon
   - GitHub：https://github.com/Treasoni/ha-addon-cn
2. 搜索 `codex` 并安装。
3. 安装完成后启动 add-on，点击「保存」并设置你的偏好选项，然后查看日志确认运行正常。

## 配置

| 配置键 | 类型 / 默认值 | 说明 |
| --- | --- | --- |
| `env_vars` | 列表 / 空 | 传入容器的额外环境变量（`name`/`value` 形式） |
| `PUID` | 整数 / 默认 `0` | 文件权限所属用户 ID |
| `PGID` | 整数 / 默认 `0` | 文件权限所属组 ID |
| `TZ` | 字符串（可选） / 空 | 长格式时区，如 `America/Los_Angeles` |
| `CODEX_RESET_ADMIN` | 整数（可选） / 空 | 将管理员用户与密码重置为默认值（设为 1） |
| `CODEX_SKIP_INTEGRITY_CHECK` | 整数（可选） / 空 | 启动时跳过数据库完整性修复（设为 1） |
| `csrf_allowed` | 字符串 / 默认 `http://homeassistant.local:8123,https://homeassistant.local:8123` | 允许访问应用的地址列表（逗号分隔） |
| `localdisks` | 字符串（可选） / 空 | 需要挂载的本地磁盘，如 `sda1,sdb1,MYNAS` |
| `networkdisks` | 字符串（可选） / 空 | 需要挂载的 SMB 共享，如 `//SERVER/SHARE` |
| `cifsusername` | 字符串（可选） / 空 | SMB 用户名 |
| `cifspassword` | 字符串（可选） / 空 | SMB 密码 |
| `cifsdomain` | 字符串（可选） / 空 | SMB 域 |

## 使用 / 访问入口

启动后可在 Home Assistant 侧边栏看到 Codex 图标，点击进入；也可通过 Web 界面端口 9810 直接访问。默认用户名与密码显示在启动日志中。

## 常见问题

- 默认用户名与密码显示在启动日志中。
- 可将主题/骨架的用户文件夹放到 `/share/codex/www/user`。
- 支持挂载本地磁盘与远程 SMB 共享。

---
- 英文原版：[Home assistant add-on: Codex](https://github.com/alexbelgium/hassio-addons/blob/master/codex/README.md)
- 来源仓库：alexbelgium
