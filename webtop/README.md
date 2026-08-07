<!-- zh-guide -->
# Webtop xfce

## 简介

Webtop 是一款可通过任何现代 Web 浏览器访问的完整 Linux 桌面环境。本加载项基于 linuxserver.io 的 docker-webtop 镜像构建，内置 Ubuntu XFCE 桌面，让浏览器即可获得完整的桌面体验。

## 安装

1. 在 Home Assistant → 设置 → 加载项 → 商店，添加本商店仓库：
   - Gitee：https://gitee.com/zhqznc_10603234_123/ha-addon
   - GitHub：https://github.com/Treasoni/ha-addon-cn
2. 搜索 webtop 并安装。

## 配置

修改配置后需要重启加载项才能生效。可选配置键如下：

| 配置键 | 类型/默认值 | 说明 |
| ------ | ----------- | ---- |
| `env_vars` | 列表，默认空 | 传入容器的自定义环境变量列表，每项包含 `name`（变量名，须匹配 `^[A-Za-z0-9_]+$`）与 `value`（变量值，可选）。 |
| `DNS_server` | 可选字符串，默认 `8.8.8.8` | 自定义 DNS 服务器。 |
| `PGID` | 整数，默认 `0` | 文件权限使用的组 ID。 |
| `PUID` | 整数，默认 `0` | 文件权限使用的用户 ID。 |
| `TZ` | 可选字符串，默认空 | 时区，例如 `Europe/London`。 |
| `additional_apps` | 可选字符串，默认 `engrampa,libreoffice` | 需要安装的软件包列表（逗号分隔）。安装的软件不会持久保留，需通过该选项在启动时安装。 |
| `DRINODE` | 枚举（`/dev/dri/card0`/`/dev/dri/card1`/`/dev/dri/card2`/`/dev/dri/renderD128`/`/dev/dri/renderD129`），默认空 | 图形设备节点。若图形显示异常，可通过此选项选择正确的 GPU 设备。 |
| `KEYBOARD` | 枚举（da-dk-qwerty/de-de-qwertz/en-gb-qwerty/en-us-qwerty/es-es-qwerty/fr-ch-qwertz/fr-fr-azerty/it-it-qwerty/ja-jp-qwerty/pt-br-qwerty/sv-se-qwerty/tr-tr-qwerty），默认空 | 桌面键盘布局。 |
| `PASSWORD` | 可选字符串，默认空 | 自定义 Web 界面访问密码。 |
| `data_location` | 可选字符串，默认空 | 自定义数据存储路径。 |
| `cifsdomain` | 可选字符串，默认空 | 网络共享（SMB）的域/工作组。 |
| `cifspassword` | 可选字符串，默认空 | 网络共享（SMB）的密码。 |
| `cifsusername` | 可选字符串，默认空 | 网络共享（SMB）的用户名。 |
| `localdisks` | 可选字符串，默认空 | 需要挂载的本地磁盘，例如 `sda1,sdb1`。 |
| `networkdisks` | 可选字符串，默认空 | 需要挂载的 SMB 网络共享，例如 `//SERVER/SHARE`。 |

## 使用 / 访问入口

- 加载项支持 Ingress，启动后可在 Home Assistant 侧边栏看到 Webtop xfce 图标，点击进入。
- Web 界面端口为 `3000/tcp`，默认关闭（宿主映射未启用），如需直接访问可在加载项端口设置中开启。**无密码直接开放端口风险极高，请务必先设置密码。**
- 默认使用 `abc` 用户，默认密码也是 `abc`。如需修改密码，可在桌面内打开终端执行 `passwd` 命令；设置密码并开启认证后，通过 `localhost:3000/?login=true` 登录访问。

## 常见问题

- **安装的软件重启后不见了？** 桌面内安装的软件不会持久保留，请通过配置中的 `additional_apps` 选项在启动时安装；软件配置（如配置文件）会保留。
- **图形显示异常或一直「等待视频流」？** 可通过 `DRINODE` 选项选择正确的 GPU 渲染节点。若日志出现 `libEGL warning: failed to open /dev/dri/card0: Permission denied`，说明当前选择的节点没有权限，请改用其他节点。
- **如何设置访问密码？** 在桌面终端执行 `passwd` 修改 `abc` 用户的密码即可；开启认证后使用带 `?login=true` 的路径访问。
- **需要自定义环境变量？** 通过 `env_vars` 选项传入，完整的可选环境变量列表参见 linuxserver.io 的 docker-webtop 文档。
- 从 4.16-r0-ls94 起外部端口默认关闭，改为依赖 Ingress 访问；从 4.16-r0-ls94-2 起内置 Microsoft Edge 安装。

---
- 英文原版：Home assistant add-on: Webtop KDE Alpine；链接 https://github.com/alexbelgium/hassio-addons/blob/master/webtop/README.md
- 来源仓库：alexbelgium
