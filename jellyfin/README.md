<!-- zh-guide -->
# Jellyfin NAS

## 简介
Jellyfin 是一套免费开源的软件媒体系统，让你自行管理并流式播放个人媒体库中的视频、音乐、直播电视与照片，支持智能电视、流媒体盒子与移动设备。本加载项基于 linuxserver.io 的 [docker-jellyfin](https://github.com/linuxserver/docker-jellyfin) 镜像，以独立的 Jellyfin 媒体服务器形式打包运行。

## 安装
1. 在 Home Assistant → 设置 → 加载项 → 商店，添加本商店仓库：
   - Gitee：https://gitee.com/zhqznc_10603234_123/homeassistant
   - GitHub：https://github.com/Treasoni/ha-addon-cn
2. 搜索 jellyfin 并安装。

## 配置

| 配置键 | 类型 / 默认值 | 说明 |
|--------|--------------|------|
| `PUID` | int，默认 `0` | 文件权限的用户 ID |
| `PGID` | int，默认 `0` | 文件权限的用户组 ID |
| `TZ` | str（可选） | 时区，例如 `Europe/London`、`Asia/Shanghai` |
| `data_location` | str，默认 `/share/jellyfin` | Jellyfin 数据存放路径；仅允许位于 `/share`、`/config`、`/data`、`/mnt` 之下，否则会重置回默认路径 |
| `localdisks` | str（可选） | 要挂载的本地磁盘，例如 `sda1,sdb1,MYNAS` |
| `networkdisks` | str（可选） | 要挂载的 SMB 共享，例如 `//SERVER/SHARE`，多个用逗号分隔 |
| `cifsusername` | str（可选） | 访问 SMB 网络共享的用户名 |
| `cifspassword` | str（可选） | 访问 SMB 网络共享的密码 |
| `cifsdomain` | str（可选） | 访问 SMB 网络共享的域名/工作组 |
| `DOCKER_MODS` | list（可选） | 硬件加速附加模块，可选值见下方「硬件加速」 |
| `env_vars` | list，默认 `[]` | 向容器传递额外环境变量（键名需匹配 `^[A-Za-z0-9_]+$`），例如 `[{name: "KEY", value: "VALUE"}]` |

### 硬件加速（DOCKER_MODS）

可选模块：
- `linuxserver/mods:jellyfin-opencl-intel` — Intel OpenCL 支持
- `linuxserver/mods:jellyfin-amd` — AMD 硬件加速
- `linuxserver/mods:jellyfin-rffmpeg` — 自定义 FFmpeg 构建

### 挂载磁盘

- 本地磁盘：参考 [Mounting Local Drives in Addons](https://github.com/alexbelgium/hassio-addons/wiki/Mounting-Local-Drives-in-Addons)
- 远程 SMB 共享：参考 [Mounting Remote Shares in Addons](https://github.com/alexbelgium/hassio-addons/wiki/Mounting-remote-shares-in-Addons)

### 自定义脚本与环境变量

本加载项支持通过 `env_vars` 选项传入额外的环境变量（键名大小写不限）。更多说明见 [Add Environment variables to your Addon](https://github.com/alexbelgium/hassio-addons/wiki/Add-Environment-variables-to-your-Addon-2)。

### 启用 HTTPS（可选）

1. 前提：已通过 Let's Encrypt 等获得 PEM 格式的证书。
2. 在终端运行 `openssl pkcs12 -export -in fullchain.pem -inkey private_key.pem -passout pass: -out server.pfx` 生成 PFX 证书文件，并执行 `chmod 0700 server.pfx`。
   > 上面的命令生成的是无密码 PFX；如需密码，可用 `-passout pass:"你的密码"`，并记得在 Jellyfin 配置中填上同一密码。
3. 打开 Jellyfin 界面：侧边栏 → `Administration` → `Dashboard`。
4. 在 `Networking` 的 `Server Address Settings` 下勾选 `Enable HTTPS`。
5. 在 `HTTPS Settings` 下勾选 `Require HTTPS`。
6. 在 `Custom SSL certificate path` 指向 PFX 文件，如有密码则填写 `Certificate password`。
7. 滚动到底部点击 `Save` 保存。

## 使用 / 访问入口
- Web 界面：通过 Home Assistant 侧边栏的 Ingress 打开，或浏览器访问 `http://<你的设备IP>:8096`。
- 额外端口（config.yaml 中定义）：`8920/tcp` 为 HTTPS Web 界面端口（可选）；`1900/udp` 用于 DLNA（可选，未对外映射）；`7359/udp` 用于服务发现（可选，未对外映射）。
- 首次访问会引导你完成服务器设置（语言、媒体库等）。
- 数据默认保存在 `/share/jellyfin`，可通过 `data_location` 调整；备份时默认排除 `cache/`、`log/`、`transcode/` 目录，避免备份过大。

## 常见问题
- **访问不了 Web 界面？** 先在加载项「日志」里确认启动是否正常，然后尝试通过侧边栏 Ingress 打开；若用 IP 访问，请确认设备与本机在同一网络、8096 端口未被占用。
- **`data_location` 不生效？** 该路径必须位于 `/share`、`/config`、`/data` 或 `/mnt` 之下，否则会被重置回默认位置。
- **播放时卡顿或硬件解码不生效？** 可在 `DOCKER_MODS` 中按 CPU 厂商选择对应的硬件加速模块（Intel / AMD / rffmpeg）后重启加载项。

---
- 英文原版：Home assistant add-on: jellyfin（链接 https://github.com/alexbelgium/hassio-addons/blob/master/jellyfin/README.md）
- 来源仓库：alexbelgium
