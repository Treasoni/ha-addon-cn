<!-- zh-guide -->
# Ubooquity

## 简介

Ubooquity 是一款免费、轻量、易于使用的漫画与电子书家庭服务器（由 vaemendis 开发），支持包括 ePUB、CBZ、CBR、PDF 在内的多种文件格式，并支持 Calibre 与 ComicRack 的元数据。它允许你为每个共享文件夹创建用户账号并设置访问权限。本加载项基于 linuxserver.io 的 docker-ubooquity 镜像构建。

## 安装

1. 在 Home Assistant → 设置 → 加载项 → 商店，添加本商店仓库：
   - Gitee：https://gitee.com/zhqznc_10603234_123/ha-addon
   - GitHub：https://github.com/Treasoni/ha-addon-cn
2. 搜索 ubooquity 并安装。

## 配置

除下列选项外，其余设置可在 Web 界面中完成。修改配置后需要重启加载项才能生效。

| 配置键 | 类型/默认值 | 说明 |
| ------ | ----------- | ---- |
| `env_vars` | 列表，默认空 | 传入容器的自定义环境变量列表，每项包含 `name`（变量名，须匹配 `^[A-Za-z0-9_]+$`）与 `value`（变量值，可选）。 |
| `PGID` | 整数，默认 `0` | 文件权限使用的组 ID。 |
| `PUID` | 整数，默认 `0` | 文件权限使用的用户 ID。 |
| `TZ` | 可选字符串，默认空 | 时区，例如 `Europe/London`。 |
| `maxmem` | 整数，默认 `200` | Java 最大内存占用（单位 MB），**关键设置**。设得太低会出现 `java.lang.OutOfMemoryError: Java heap space` 错误；设得太高可能拖垮系统导致 Home Assistant 崩溃。 |
| `ssl` | 布尔，默认 `false` | 是否启用 HTTPS。 |
| `certfile` | 字符串，默认 `fullchain.pem` | TLS 证书文件，需存放在 `/ssl/` 目录。 |
| `keyfile` | 字符串，默认 `privkey.pem` | TLS 私钥文件，需存放在 `/ssl/` 目录。 |
| `theme` | 枚举（default/comixology2/plextheme-master），默认 `default` | Web 界面主题。 |
| `cifsdomain` | 可选字符串，默认空 | 网络共享（SMB）的域/工作组。 |
| `cifspassword` | 可选字符串，默认空 | 网络共享（SMB）的密码。 |
| `cifsusername` | 可选字符串，默认空 | 网络共享（SMB）的用户名。 |
| `localdisks` | 可选字符串，默认空 | 需要挂载的本地磁盘，例如 `sda1,sdb1,MYNAS`。 |
| `networkdisks` | 可选字符串，默认空 | 需要挂载的 SMB 网络共享，例如 `//SERVER/SHARE`（多个用逗号分隔，挂载到 `/mnt/$sharename`）。 |
| `smbv1` | 可选布尔，默认空 | 是否启用 SMB v1 协议。 |

## 使用 / 访问入口

本加载项不提供 Ingress，通过端口访问：

- 图书库页面：`2205/tcp`（映射到宿主端口 `2202`），对外提供服务时暴露此端口。
- 管理页面：`2206/tcp`（映射到宿主端口 `2203`），仅在本地使用，路径为 `/ubooquity/admin`。

首次打开 Web 界面后，请设置管理员密码并根据提示完成管理选项配置。默认用户名/密码会显示在加载项启动日志中。

## 常见问题

- **`maxmem` 设置不当会有什么后果？** 设得太低，执行高内存操作时会遇到 `java.lang.OutOfMemoryError: Java heap space` 错误；设得太高可能使系统崩溃，需要手动重启 Home Assistant。建议树莓派 3B+ 用默认 `200`MB，内存 2GB 以上的设备推荐 `512`MB。
- **如何在手机上看漫画/电子书？** 建议在 Ubooquity 中启用 OPDS 服务器，然后用支持 OPDS 的阅读 App 连接，例如 iOS 上的 Chunky、Android 上的 Kuboo。
- **默认账号密码是什么？** 首次启动后，默认用户名/密码显示在加载项「日志」中。
- **如何挂载本地磁盘或远程共享？** 分别通过 `localdisks` 与 `networkdisks` 配置，详细步骤参见上游 wiki「Mounting Local Drives in Addons」与「Mounting Remote Shares in Addons」。注意挂载磁盘会略微降低性能。
- Home Assistant 项目已弃用 armv7、armhf 与 i386 架构支持，将在 Home Assistant 2025.12 版本中完全移除。

---
- 英文原版：Home assistant add-on: Ubooquity；链接 https://github.com/alexbelgium/hassio-addons/blob/master/ubooquity/README.md
- 来源仓库：alexbelgium
