<!-- zh-guide -->
# Emby

## 简介
Emby 是一款免费的媒体服务系统，帮你整理个人媒体库中的视频、音乐、直播电视和照片，并串流到智能电视、电视盒子与移动设备。本加载项以独立的 Emby 媒体服务器形式打包，基于 linuxserver.io 的 docker-emby 镜像构建。

## 安装
1. 在 Home Assistant → 设置 → 加载项 → 商店，添加本商店仓库：
   - Gitee：https://gitee.com/zhqznc_10603234_123/ha-addon
   - GitHub：https://github.com/Treasoni/ha-addon-cn
2. 搜索 emby 并安装。

## 配置
安装后请先保存配置再启动加载项，并留意日志确认一切正常。以下是本加载项的配置项（仅列出真实存在的键）：

| 配置键 | 类型/默认值 | 说明 |
|--------|-------------|------|
| `PUID` | int / `0` | 文件权限的用户 ID |
| `PGID` | int / `0` | 文件权限的组 ID |
| `TZ` | str / 空 | 时区，例如 `Europe/London` |
| `localdisks` | str / 空 | 要挂载的本地磁盘，例如 `sda1,sdb1`（也可用磁盘标签） |
| `networkdisks` | str / 空 | 要挂载的 SMB 共享，例如 `//SERVER/SHARE`，多个用逗号分隔 |
| `cifsusername` | str / 空 | 访问 SMB 共享的用户名 |
| `cifspassword` | str / 空 | 访问 SMB 共享的密码 |
| `cifsdomain` | str / 空 | SMB 共享所在的域 |
| `smbv1` | bool / `false` | 是否启用 SMB v1 协议 |
| `silent` | bool / `true` | 是否隐藏 Emby 服务器的调试日志；排查问题时建议关闭 |
| `env_vars` | 列表 / `[]` | 以"名称/值"形式传递额外的环境变量，用于注入配置文件中未提供的变量 |

- 使用 `env_vars` 可追加任意环境变量（名称需匹配 `^[A-Za-z0-9_]+$`），详见上游 Wiki：[Add-Environment-variables-to-your-Addon-2](https://github.com/alexbelgium/hassio-addons/wiki/Add-Environment-variables-to-your-Addon-2)。
- 本地磁盘挂载参见 [Mounting Local Drives in Addons](https://github.com/alexbelgium/hassio-addons/wiki/Mounting-Local-Drives-in-Addons)，远程 SMB 共享挂载参见 [Mounting Remote Shares in Addons](https://github.com/alexbelgium/hassio-addons/wiki/Mounting-remote-shares-in-Addons)。

### 配置示例

```yaml
PGID: 0
PUID: 0
TZ: "Europe/London"
localdisks: "sda1,sdb1"
networkdisks: "//192.168.1.100/media,//nas.local/movies"
cifsusername: "mediauser"
cifspassword: "password123"
cifsdomain: "workgroup"
silent: false
```

## 使用 / 访问入口
- **Ingress 入口**：加载项内置 Ingress，可在 Home Assistant 中直接点击"打开 Web UI"访问，无需额外端口。
- **Web 界面端口**：`8096/tcp`，可通过 `http://<你的IP>:8096` 访问。
- **可选端口**：`8920/tcp`（HTTPS Web 界面）、`1900/udp`（DLNA）、`7359/udp`（服务发现），均为可选，默认不对外映射。
- 加载项使用 host 网络模式，便于启用 UPNP、Chromecast 等功能。
- 媒体库数据默认存放于 `/config/database`，配置存放于 `/config/emby`，并预置了 `/media`、`/share` 等挂载点，方便整理媒体文件。

## 常见问题
- **看不到 Emby 的日志输出？** `silent` 默认开启会隐藏调试信息，如需排查问题请在配置中关闭 `silent` 后重启加载项。
- **如何挂载媒体磁盘？** 本地磁盘用 `localdisks`（多个以逗号分隔，支持磁盘标签），远程 SMB 共享用 `networkdisks` 配合 `cifsusername`/`cifspassword`/`cifsdomain`。
- **如何在 Home Assistant 外访问？** 通过 `http://<你的IP>:8096` 直接访问；如需 HTTPS，可映射可选端口 `8920/tcp`。

---
- 英文原版：[Home assistant add-on: emby](https://github.com/alexbelgium/hassio-addons/blob/master/emby/README.md)
- 来源仓库：alexbelgium
