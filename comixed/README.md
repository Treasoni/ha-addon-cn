<!-- zh-guide -->
# Comixed

## 简介

ComiXed 是一个跨平台的数字漫画管理应用，专为管理大型数字漫画库而设计，支持漫画库整理、从 Comic Vine 抓取元数据、创建与管理阅读列表、基于 Web 的阅读界面，以及 CBZ、CBR、CB7、PDF 等多种漫画格式。

## 安装

1. 在 Home Assistant → 设置 → 加载项 → 商店，添加本商店仓库：
   - Gitee：https://gitee.com/zhqznc_10603234_123/ha-addon
   - GitHub：https://github.com/Treasoni/ha-addon-cn
2. 搜索 `comixed` 并安装。
3. 安装完成后启动 add-on，点击「保存」并设置你的偏好选项，然后查看日志确认运行正常。

## 配置

| 配置键 | 类型 / 默认值 | 说明 |
| --- | --- | --- |
| `env_vars` | 列表 / 空 | 传入容器的额外环境变量（`name`/`value` 形式） |
| `TZ` | 字符串（可选） / 空 | 时区，如 `Europe/London` |
| `localdisks` | 字符串（可选） / 空 | 需要挂载的本地磁盘，如 `sda1,sdb1,MYNAS` |
| `networkdisks` | 字符串（可选） / 空 | 需要挂载的 SMB 共享，如 `//SERVER/SHARE` |
| `cifsusername` | 字符串（可选） / 空 | SMB 用户名 |
| `cifspassword` | 字符串（可选） / 空 | SMB 密码 |
| `cifsdomain` | 字符串（可选） / 空 | SMB 域 |

## 使用 / 访问入口

Web 界面可通过 `http://<宿主地址>:7171` 访问（端口 7171）。首次启动需要先在 Web 界面中创建管理员账户。

## 常见问题

- 支持漫画库管理与整理、从 Comic Vine 抓取元数据、阅读列表管理与基于 Web 的阅读界面。
- 支持 CBZ、CBR、CB7、PDF 等多种漫画格式，并支持用户管理与权限。

---
- 英文原版：[Home assistant add-on: Comixed](https://github.com/alexbelgium/hassio-addons/blob/master/comixed/README.md)
- 来源仓库：alexbelgium
