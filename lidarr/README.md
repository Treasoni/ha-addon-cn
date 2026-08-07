<!-- zh-guide -->
# Lidarr NAS

## 简介
Lidarr NAS 是一款面向 Usenet 和 BitTorrent 用户的音乐收藏管理工具。它可以监控多个 RSS 订阅源，为你喜爱的艺术家自动抓取新专辑，并配合下载客户端和索引器完成下载、整理与重命名；当出现更高质量的版本时，还能自动升级库中已有文件的品质。本加载项基于 linuxserver 的 docker-lidarr 镜像构建。

## 安装
1. 在 Home Assistant → 设置 → 加载项 → 商店，添加本商店仓库：
   - Gitee：https://gitee.com/zhqznc_10603234_123/ha-addon
   - GitHub：https://github.com/Treasoni/ha-addon-cn
2. 搜索 **lidarr** 并安装。
3. 安装后在配置页设置所需选项，点击「保存」，然后启动加载项。
4. 查看加载项日志确认启动正常，再打开 Web 界面完成后续设置。

## 配置
除下表所列选项外，其余设置都可以直接在 Lidarr 的 Web 界面中完成。

| 配置键 | 类型/默认值 | 说明 |
|--------|-------------|------|
| `env_vars` | 数组，默认 `[]` | 追加额外的环境变量；每个条目含 `name`（须匹配 `^[A-Za-z0-9_]+$`）与可选的 `value` |
| `PGID` | int，默认 `0` | 用于文件权限的组 ID |
| `PUID` | int，默认 `0` | 用于文件权限的用户 ID |
| `TZ` | str（可选） | 时区，例如 `Europe/London` |
| `localdisks` | str（可选） | 需要挂载的本地磁盘，例如 `sda1,sdb1,MYNAS` |
| `networkdisks` | str（可选） | 需要挂载的 SMB 共享，例如 `//SERVER/SHARE` |
| `cifsusername` | str（可选） | 访问网络共享的 SMB 用户名 |
| `cifspassword` | str（可选） | 访问网络共享的 SMB 密码 |
| `cifsdomain` | str（可选） | 访问网络共享的 SMB 域/工作组 |

## 使用 / 访问入口
- 启动后通过 Web 界面访问：`http://homeassistant:8686`（端口 8686 已映射到宿主机）；上游文档也提到可通过侧边栏 Ingress 进入。
- 首次使用：打开 Web 界面，在 Lidarr 应用内配置索引器、下载客户端与音乐库路径，日常调整也都在应用内完成。
- 加载项会挂载 Home Assistant 的 `share` 与 `media` 目录，并自动创建 `/share/music`、`/share/downloads` 文件夹，用于存放音乐与下载文件。
- 本加载项基于 linuxserver/docker-lidarr 镜像，默认配置了 `DOCKER_MODS=linuxserver/mods:lidarr-flac2mp3` 模组（用于在导入时把 FLAC 转码为 MP3）。

## 常见问题
1. **配置文件在哪里？** 自较新版本起，配置目录已迁移到 `/addon_configs/xxx-lidarr_nas`（该目录只能通过 Filebrowser 等加载项访问），不再直接写入 Home Assistant 的配置目录；旧数据会自动迁移，但请记得更新所有相关链接。
2. **文件权限不对怎么办？** 遇到读写权限问题时，把 `PUID` / `PGID` 设为与你用户一致的 ID 即可。
3. **如何挂载磁盘？** 本地磁盘用 `localdisks`（填盘符或标签，如 `sda1`）；网络共享用 `networkdisks`，并配合 `cifsusername`、`cifspassword`、`cifsdomain` 使用。
4. **支持哪些架构？** 仅支持 aarch64 与 amd64；armv7、armhf、i386 已不再提供支持。

---
- 英文原版：Home assistant add-on: Lidarr；链接 https://github.com/alexbelgium/hassio-addons/blob/master/lidarr/README.md
- 来源仓库：alexbelgium
