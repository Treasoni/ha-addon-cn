<!-- zh-guide -->
# Plex NAS

## 简介

本加载项把 Plex 打包成独立的媒体服务器（Plex Media Server），帮你整理个人媒体库中的视频、音乐、照片与直播电视，并串流到智能电视、电视盒子、手机等设备。镜像基于 [linuxserver.io 的 docker-plex](https://github.com/linuxserver/docker-plex)，并额外加入最新 Beta 版本、SMB 网络共享挂载与本地磁盘挂载支持。

## 安装

1. 在 Home Assistant → 设置 → 加载项 → 商店，添加本商店仓库：
   - Gitee：https://gitee.com/zhqznc_10603234_123/ha-addon
   - GitHub：https://github.com/Treasoni/ha-addon-cn
2. 搜索 plex 并安装。

## 配置

核心配置项如下表。保存配置后启动加载项，并留意日志确认一切正常。

| 配置键 | 类型/默认值 | 说明 |
|--------|------------|------|
| `PUID` | int / `0` | 文件权限的用户 ID |
| `PGID` | int / `0` | 文件权限的组 ID |
| `TZ` | str / 空 | 时区，例如 `Europe/London` |
| `claim` | str / `Get_from_https://www.plex.tv/claim` | Plex 认领令牌，从 https://plex.tv/claim 获取 |
| `data_location` | str / `/share/plex` | Plex 数据的存储路径 |
| `localdisks` | str / 空 | 要挂载的本地磁盘，逗号分隔，如 `sda1,sdb1,MYNAS` |
| `networkdisks` | str / 空 | 要挂载的 SMB 共享，如 `//SERVER/SHARE` |
| `cifsusername` | str / 空 | 网络共享（SMB）用户名 |
| `cifspassword` | str / 空 | 网络共享（SMB）密码 |
| `cifsdomain` | str / 空 | 网络共享（SMB）域 |
| `smbv1` | bool / `false` | 启用 SMB v1 协议 |
| `skip_permissions_check` | bool / `false` | 跳过文件权限检查，可加速启动 |
| `clear_codecs_folder` | bool / 空 | 启用后启动时清除 Codecs 文件夹 |
| `env_vars` | 列表 | 额外传给容器的环境变量（名称须匹配 `^[A-Za-z0-9_]+$`） |

说明：

- **数据目录迁移**：修改 `data_location` 时，若目标文件夹为空，加载项会自动把旧位置的数据复制过来（旧位置通过 `/config/Library` 符号链接识别，首次迁移时默认为 `/share/plex`）；若目标已有 Plex 数据则跳过迁移，避免覆盖。
- **挂载磁盘**：支持挂载本地磁盘与远程 SMB 共享，分别参考 [挂载本地磁盘](https://github.com/alexbelgium/hassio-addons/wiki/Mounting-Local-Drives-in-Addons) 与 [挂载远程共享](https://github.com/alexbelgium/hassio-addons/wiki/Mounting-remote-shares-in-Addons)。
- 额外环境变量可通过 `env_vars` 传入，详见 [Add-Environment-variables-to-your-Addon-2](https://github.com/alexbelgium/hassio-addons/wiki/Add-Environment-variables-to-your-Addon-2)。

示例配置：

```yaml
PUID: 0
PGID: 0
TZ: "Europe/London"
claim: "Get_from_https://www.plex.tv/claim"
localdisks: "sda1,sdb1"
networkdisks: "//192.168.1.100/media,//nas.local/movies"
cifsusername: "mediauser"
cifspassword: "password123"
cifsdomain: "workgroup"
data_location: "/share/plex"
```

## 使用 / 访问入口

- 加载项使用主机网络（host network），Web 界面访问地址为 `http://<你的IP>:32400/web`（浏览器打开 `http://<你的IP>:32400` 即可）。
- 首次使用需在配置中填写 `claim` 认领令牌：访问 https://www.plex.tv/claim，把生成的令牌填入后重启加载项完成认领。
- 常用的 Plex 端口：`32400`（Plex 媒体服务器界面）、`32469`（DLNA）、`8324`（Plex for Roku / Plex Companion）、`3005`（Plex Home Theater）、`32410`-`32414`（GDM 网络发现）、`1900`（DLNA）、`33400`/`33443`（WebTools）。

## 常见问题

- **无法认领服务器**：`claim` 令牌必须来自 https://www.plex.tv/claim 且有效，填好后需重启加载项生效。
- **媒体目录读取不到文件**：检查 `PUID`/`PGID` 是否正确，或勾选 `skip_permissions_check` 跳过权限检查；本地磁盘与 SMB 共享需通过 `localdisks`/`networkdisks` 配置挂载。
- **更换数据盘后数据丢失**：修改 `data_location` 且目标文件夹非空时不会自动迁移，请先清空目标目录或手动复制旧数据。

---
- 英文原版：Home assistant add-on: plex（链接 https://github.com/alexbelgium/hassio-addons/blob/master/plex/README.md）
- 来源仓库：alexbelgium
