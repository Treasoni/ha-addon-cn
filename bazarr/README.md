<!-- zh-guide -->
# Bazarr NAS

## 简介
Bazarr 是 Sonarr 和 Radarr 的配套应用，负责根据你的需求自动下载和管理字幕。本加载项基于 linuxserver/docker-bazarr 镜像构建，支持通过侧边栏 Ingress 直接访问 WebUI。

## 安装
1. 在 Home Assistant → 设置 → 加载项 → 商店，添加本商店仓库：
   - Gitee：https://gitee.com/zhqznc_10603234_123/homeassistant
   - GitHub：https://github.com/Treasoni/ha-addon-cn
2. 搜索 bazarr 并安装。

## 配置
除下表列出的选项外，其余设置均可直接在应用的 WebUI 中完成。

| 配置键 | 类型/默认值 | 说明 |
|--------|-------------|------|
| `PGID` | int / `0` | 文件权限组 ID |
| `PUID` | int / `0` | 文件权限用户 ID |
| `TZ` | str / 空 | 时区（如 `Europe/London`） |
| `connection_mode` | list / `ingress_noauth` | 连接模式：`ingress_noauth` / `noingress_auth` / `ingress_auth` |
| `localdisks` | str / 空 | 要挂载的本地磁盘（如 `sda1,sdb1,MYNAS`） |
| `networkdisks` | str / 空 | 要挂载的 SMB 共享（如 `//SERVER/SHARE`） |
| `cifsusername` | str / 空 | SMB 网络共享用户名 |
| `cifspassword` | str / 空 | SMB 网络共享密码 |
| `cifsdomain` | str / 空 | SMB 网络共享域 |
| `env_vars` | list / `[]` | 额外传给容器的环境变量（键名需匹配 `^[A-Za-z0-9_]+$`） |

连接模式说明：
- `ingress_noauth`（默认）：关闭认证，与侧边栏 Ingress 无缝集成
- `noingress_auth`：关闭 Ingress，改为通过外部 URL 访问并启用认证
- `ingress_auth`：同时启用 Ingress 与认证

## 使用 / 访问入口
- 通过侧边栏 Ingress 进入（入口路径 `bazarr`），或访问 `http://homeassistant:6767`。
- 首次启动后打开 WebUI，按需连接 Sonarr/Radarr 并设置字幕下载偏好。
- 加载项会自动创建 `/share/storage/movies`、`/share/storage/tv`、`/share/downloads` 目录用于存放媒体与下载内容。
- 可通过 `localdisks` 挂载本地磁盘，或通过 `networkdisks` 挂载远程 SMB 共享。

## 常见问题
- **为什么从侧边栏 Ingress 访问时无需登录？** 默认 `ingress_noauth` 模式会关闭认证以便无缝集成；如需认证，请切换到 `noingress_auth` 或 `ingress_auth`，并注意不要让端口暴露到公网以免造成安全风险。
- **为什么配置目录被迁移了？** 从 1.5.4 起配置目录迁移到仅加载项可访问的 `/addon_configs/xxx-bazarr`，避免污染 Home Assistant 配置目录；迁移会自动完成，但请更新相关的链接/路径。
- **Ingress 访问时出现重定向或 HTTPS 混合内容问题？** 新版本已修复 nginx 将重定向改写成绝对 URL、导致 HTTPS 下被浏览器拦截的问题。

---
- 英文原版：Home assistant add-on: bazarr（链接 https://github.com/alexbelgium/hassio-addons/blob/master/bazarr/README.md）
- 来源仓库：alexbelgium
