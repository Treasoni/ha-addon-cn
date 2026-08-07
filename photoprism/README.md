<!-- zh-guide -->
# Photoprism

## 简介
Photoprism 是一个基于服务器的应用，用于浏览、整理和分享你的个人照片收藏。它随 Home Assistant 以加载项形式运行，可通过侧边栏 Ingress 直接访问。项目主页：https://github.com/photoprism/photoprism

## 安装
1. 在 Home Assistant → 设置 → 加载项 → 商店，添加本商店仓库：
   - Gitee：https://gitee.com/zhqznc_10603234_123/ha-addon
   - GitHub：https://github.com/Treasoni/ha-addon-cn
2. 搜索 photoprism 并安装。

## 配置
支持架构：aarch64、amd64。该加载项基于官方 Photoprism 镜像构建，提供 Ingress 侧边栏入口与 Web 界面。

> 系统要求：至少 **2 核 CPU + 4GB 内存**，否则加载项可能无法正常运行。

| 配置键 | 类型/默认值 | 说明 |
|--------|------|------|
| `ssl` | bool，默认 `false` | 为 Web 界面启用 HTTPS |
| `certfile` | str，默认 `fullchain.pem` | SSL 证书文件（需位于 `/ssl`） |
| `keyfile` | str，默认 `privkey.pem` | SSL 私钥文件（需位于 `/ssl`） |
| `DB_TYPE` | list，默认 `sqlite` | 数据库类型：`sqlite`（本地）/ `mariadb_addon`（使用 MariaDB 加载项）/ `external`（外部数据库） |
| `ORIGINALS_PATH` | str，默认 `/share/photoprism/originals` | 照片和视频原始文件存放目录 |
| `STORAGE_PATH` | str，默认 `/share/photoprism/storage` | 缓存、数据库和 sidecar 文件目录 |
| `IMPORT_PATH` | str，默认 `/share/photoprism/import` | 导入文件目录 |
| `BACKUP_PATH` | str，默认 `/share/photoprism/backup` | 备份存放目录 |
| `UPLOAD_NSFW` | bool，默认 `true` | 是否允许上传可能冒犯性（NSFW）的内容 |
| `graphic_drivers` | list，可选（`mesa`） | 图形驱动选择 |
| `ingress_disabled` | bool，可选 | 设为 `true` 时禁用 Ingress，改用 IP:端口 直接访问 |
| `localdisks` | str，可选 | 要挂载的本地磁盘，多个用逗号分隔（如 `sda1,sdb1,MYNAS`） |
| `networkdisks` | str，可选 | 要挂载的 SMB 共享（如 `//服务器/共享名`） |
| `cifsusername` | str，可选 | 访问网络共享的 SMB 用户名 |
| `cifspassword` | str，可选 | 访问网络共享的 SMB 密码 |
| `cifsdomain` | str，可选 | 访问网络共享的 SMB 域/工作组 |
| `env_vars` | array，默认 `[]` | 以 name/value 形式追加额外环境变量 |
| `CONFIG_LOCATION` | str，默认 `/config` | 配置文件位置（新版自动迁移到 `/addon_configs/xxx-photoprism/`） |

> 迁移说明：配置文件现在存放在 `/addon_configs/xxx-photoprism/` 下。加载项会自动把旧位置 `/config/addons_config/photoprism/` 的文件迁移过来，但任何指向旧位置的自定义路径、脚本或备份都需要手动更新。升级前请先备份，以防自定义路径或权限导致迁移失败。

### 高级配置
可在 `/addon_configs/xxx-photoprism/config.yaml` 中追加更多 Photoprism 配置项（完整变量清单见 [photoprism docker-compose.yml](https://github.com/photoprism/photoprism/blob/develop/docker-compose.yml)）。

使用外部数据库时，在配置文件中追加：

```yaml
PHOTOPRISM_DATABASE_DRIVER: "mysql"
PHOTOPRISM_DATABASE_SERVER: "IP:PORT"
PHOTOPRISM_DATABASE_NAME: "photoprism"
PHOTOPRISM_DATABASE_USER: "USERNAME"
PHOTOPRISM_DATABASE_PASSWORD: "PASSWORD"
```

选择 `mariadb_addon` 时，需先安装并启动 MariaDB 加载项，加载项会自动发现并连接。

### 挂载磁盘
- 本地磁盘：参考 [Mounting Local Drives in Addons](https://github.com/alexbelgium/hassio-addons/wiki/Mounting-Local-Drives-in-Addons)
- SMB 远程共享：参考 [Mounting Remote Shares in Addons](https://github.com/alexbelgium/hassio-addons/wiki/Mounting-remote-shares-in-Addons)

## 使用 / 访问入口
- **Web 界面**：通过 Home Assistant 侧边栏的 Ingress 入口访问，或直接访问 `http://homeassistant:2342`（端口 `2342`）。
- **默认凭据**：用户名 `admin`，密码 `please_change_password`。首次登录后请务必修改密码。
- **启动提示**：加载项启动需等待约 1–2 分钟，日志出现绿色提示后即可访问。
- **WebDAV 访问**：使用 `http://本地IP:端口/api/hassio.../originals` 访问原始照片（完整路径见加载项日志）。
- **命令行界面**：可通过 Portainer 加载项，或用 SSH 执行 `docker exec -it <photoprism 容器 id> bash` 进入。**注意**：不要使用 `docker exec <容器 id> photoprism`，这会导致不可预知的行为。

## 常见问题
- **启动失败或卡顿**：请确认设备满足最低 2 核 CPU + 4GB 内存的要求；使用 `mariadb_addon` 时需先安装并启动 MariaDB 加载项，卸载 MariaDB 会删除其数据。
- **升级后路径失效**：新版本配置文件已迁移到 `/addon_configs/xxx-photoprism/`，请更新所有指向旧路径 `/config/addons_config/photoprism/` 的链接和备份。
- **自定义环境变量**：可通过 `env_vars` 选项或在 `config.yaml` 中追加 `PHOTOPRISM_*` 变量，无需改动加载项本身。

---
- 英文原版：[Home assistant add-on: Photoprism](https://github.com/alexbelgium/hassio-addons/blob/master/photoprism/README.md)
- 来源仓库：alexbelgium
