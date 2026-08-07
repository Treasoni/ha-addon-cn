<!-- zh-guide -->
# ResilioSync

## 简介

Resilio Sync 是一个自托管的网页文件共享与协作平台，采用点对点同步技术，无需经过第三方服务器即可在设备间直接同步文件。本加载项基于 linuxserver.io 的 Resilio Sync 镜像构建。

## 安装

1. 在 Home Assistant → 设置 → 加载项 → 商店，添加本商店仓库：
   - Gitee：https://gitee.com/zhqznc_10603234_123/ha-addon
   - GitHub：https://github.com/Treasoni/ha-addon-cn
2. 搜索 `resiliosync` 并安装。

## 配置

| 配置键 | 类型 / 默认值 | 说明 |
|--------|--------------|------|
| `env_vars` | 列表 / 空 | 额外环境变量列表（每项含 `name` 和 `value`），用于向容器传递自定义环境变量 |
| `PGID` | 整数 / 默认 `0` | 文件权限组 ID |
| `PUID` | 整数 / 默认 `0` | 文件权限用户 ID |
| `config_location` | 字符串 / 默认 `/config/addons_config/resiliosync` | 配置文件的存放位置 |
| `data_location` | 字符串 / 默认 `/share/resiliosync` | 同步数据的存放位置 |
| `downloads_location` | 字符串 / 默认 `/share/resiliosync_downloads` | 下载文件的存放位置 |
| `TZ` | 字符串 / 空 | 时区（如 `Europe/London`） |
| `localdisks` | 字符串 / 空 | 要挂载的本地磁盘（如 `sda1,sdb1,MYNAS`） |
| `networkdisks` | 字符串 / 空 | 要挂载的 SMB 共享（如 `//SERVER/SHARE`） |
| `cifsusername` | 字符串 / 空 | SMB 共享用户名 |
| `cifspassword` | 字符串 / 空 | SMB 共享密码 |
| `cifsdomain` | 字符串 / 空 | SMB 共享域名 |

## 使用 / 访问入口

启动后可在 Home Assistant 侧边栏看到 ResilioSync 图标，点击进入。Web 界面位于宿主端口 8888，同步端口为 55555。

## 常见问题

- **如何挂载磁盘**：支持挂载本地磁盘与远程 SMB 共享，分别通过 `localdisks` 和 `networkdisks` 以及 `cifsusername`/`cifspassword`/`cifsdomain` 选项配置。
- **数据与配置路径**：默认同步数据存放在 `/share/resiliosync`，配置文件存放在 `/config/addons_config/resiliosync`，可通过 `data_location` 与 `config_location` 调整。
- **如何添加自定义环境变量**：可通过 `env_vars` 选项向容器传递额外的环境变量。

---
- 英文原版：[Resilio Sync](https://github.com/alexbelgium/hassio-addons/blob/master/resiliosync/README.md)
- 来源仓库：alexbelgium
