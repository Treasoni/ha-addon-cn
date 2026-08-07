<!-- zh-guide -->
# Readarr

## 简介

Readarr 是一个面向 Usenet 和 BitTorrent 用户的电子书收藏管理器（相当于「电子书版的 Sonarr」）。它可以监控多个 RSS 源，自动获取你喜爱的作者发布的新书，并与下载客户端和索引器协同完成书籍的获取、整理和重命名。本加载项基于 linuxserver/docker-readarr 镜像构建。

## 安装

1. 在 Home Assistant → 设置 → 加载项 → 商店，添加本商店仓库：
   - Gitee：https://gitee.com/zhqznc_10603234_123/ha-addon
   - GitHub：https://github.com/Treasoni/ha-addon-cn
2. 搜索 `readarr` 并安装。

## 配置

大部分配置可直接在应用网页界面中完成，以下选项可在加载项配置中设置。

| 配置键 | 类型 / 默认值 | 说明 |
|--------|--------------|------|
| `env_vars` | 列表 / 空 | 额外环境变量列表（每项含 `name` 和 `value`），用于向容器传递自定义环境变量 |
| `PGID` | 整数 / 默认 `0` | 文件权限组 ID |
| `PUID` | 整数 / 默认 `0` | 文件权限用户 ID |
| `connection_mode` | 枚举（ingress_noauth / noingress_auth / ingress_auth）/ 默认 `ingress_noauth` | 连接模式：`ingress_noauth` 关闭认证以无缝接入 Ingress；`noingress_auth` 关闭 Ingress 以使用外部 URL 并启用认证；`ingress_auth` 同时启用 Ingress 与认证 |
| `TZ` | 字符串 / 空 | 时区（如 `Europe/London`） |
| `localdisks` | 字符串 / 空 | 要挂载的本地磁盘（如 `sda1,sdb1,MYNAS`） |
| `networkdisks` | 字符串 / 空 | 要挂载的 SMB 共享（如 `//SERVER/SHARE`） |
| `cifsusername` | 字符串 / 空 | SMB 共享用户名 |
| `cifspassword` | 字符串 / 空 | SMB 共享密码 |
| `cifsdomain` | 字符串 / 空 | SMB 共享域名 |

## 使用 / 访问入口

启动后可在 Home Assistant 侧边栏看到 Readarr 图标，点击进入。也可直接通过浏览器访问宿主机的 8787 端口（Web 界面）。

## 常见问题

- **连接模式如何选择**：默认 `ingress_noauth` 适合通过侧边栏 Ingress 无缝访问；如需通过外部地址直接访问，建议使用 `noingress_auth` 以启用认证保护。
- **配置目录在哪**：自 0.4.18-1 起配置默认存放在 `/addon_configs/xxx-readarr_nas`（仅可通过 Filebrowser 加载项访问），该目录随加载项备份一起保存。请更新所有指向旧配置路径的链接。
- **如何挂载磁盘**：支持挂载本地磁盘与远程 SMB 共享，分别通过 `localdisks` 和 `networkdisks` 以及 `cifsusername`/`cifspassword`/`cifsdomain` 选项配置。
- **如何添加自定义环境变量**：可通过 `env_vars` 选项，或直接在 `/addon_configs/xxx-readarr_nas/readarr_nas.yml` 中写入自定义变量。

---
- 英文原版：[Readarr](https://github.com/alexbelgium/hassio-addons/blob/master/readarr/README.md)
- 来源仓库：alexbelgium
