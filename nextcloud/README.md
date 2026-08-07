<!-- zh-guide -->
# Nextcloud

## 简介

Nextcloud 是一款开源的自托管云存储与协作平台，可让你在自己的服务器上同步文件、分享内容并使用各种云端应用。本加载项基于 linuxserver.io 的 [docker-nextcloud](https://github.com/linuxserver/docker-nextcloud) 镜像构建，额外集成了 OCR、全文搜索、缩略图、本地/网络磁盘挂载等配置能力，并针对 Home Assistant 做了适配（当前版本 34.0.2，支持 aarch64 / amd64 架构）。

## 安装

1. 在 Home Assistant → 设置 → 加载项 → 商店，添加本商店仓库：
   - Gitee：https://gitee.com/zhqznc_10603234_123/ha-addon
   - GitHub：https://github.com/Treasoni/ha-addon-cn
2. 搜索 nextcloud 并安装。
3. 点击"保存"保存配置，然后启动加载项。
4. 查看日志确认启动是否正常，再打开 Web 界面完成首次配置（创建管理员账号、密码与数据库）。
5. 如需让某些选项生效，重启加载项一次。

## 配置

Web 界面通过 `https://<主机地址>:<端口>` 访问（默认端口 8099）。配置键如下，仅列出真实存在的选项：

| 配置键 | 类型 / 默认值 | 说明 |
|--------|--------------|------|
| `PUID` | int / `1000` | 文件权限对应的用户 ID |
| `PGID` | int / `1000` | 文件权限对应的组 ID |
| `TZ` | str / 空 | 时区（如 `Europe/London`） |
| `env_vars` | list / `[]` | 追加环境变量（名称需匹配 `^[A-Za-z0-9_]+$`） |
| `additional_apps` | str / `inotify-tools` | 额外安装的 APK 软件包（逗号分隔） |
| `trusted_domains` | str / 空 | 允许访问 Nextcloud 的信任域名或 IP（逗号分隔） |
| `use_own_certs` | bool / `false` | 是否使用自备的 SSL 证书 |
| `certfile` | str / `fullchain.pem` | SSL 证书文件名（位于 `/ssl/` 目录） |
| `keyfile` | str / `privkey.pem` | SSL 私钥文件名（位于 `/ssl/` 目录） |
| `OCR` | bool / `false` | 启用 Tesseract OCR 文字识别能力 |
| `OCRLANG` | str / `fra` | OCR 识别语言（如 `fra,eng`，逗号分隔） |
| `Full_Text_Search` | bool / `false` | 启用基于 Elasticsearch 的全文搜索 |
| `elasticsearch_server` | str / 空 | Elasticsearch 服务器地址（`ip:port`） |
| `enable_thumbnails` | bool / `true` | 是否生成文件缩略图 |
| `default_phone_region` | str / 空 | 默认手机区号（ISO 3166-1 alpha-2，如 `CN`） |
| `disable_updates` | bool / `false` | 禁止 Nextcloud 应用自动更新 |
| `env_memory_limit` | str / `512M` | PHP 内存上限 |
| `env_post_max_size` | str / `512M` | POST 请求体大小上限 |
| `env_upload_max_filesize` | str / `512M` | 上传文件大小上限 |
| `localdisks` | str / 空 | 要挂载的本地磁盘（如 `sda1,sdb1,MYNAS`） |
| `networkdisks` | str / 空 | 要挂载的 SMB 网络共享（如 `//SERVER/SHARE`） |
| `cifsusername` | str / 空 | SMB 共享的用户名 |
| `cifspassword` | str / 空 | SMB 共享的密码 |
| `cifsdomain` | str / 空 | SMB 共享的域 |
| `skip_permissions_check` | bool / `false` | 跳过启动时的文件权限检查（数据盘较大时启动更快的替代方案） |

### 挂载磁盘

- **本地磁盘**：参见 [Mounting Local Drives in Addons](https://github.com/alexbelgium/hassio-addons/wiki/Mounting-Local-Drives-in-Addons)
- **远程 SMB 共享**：参见 [Mounting Remote Shares in Addons](https://github.com/alexbelgium/hassio-addons/wiki/Mounting-remote-shares-in-Addons)

### 自定义脚本与环境变量

- 自定义启动脚本：把脚本放到 `/config/addons_autoscripts/nextcloud-ocr.sh`，会在初始化完成后执行（例如可用于 `occ files:scan --all` 扫描文件）。
- 额外环境变量：通过 `env_vars` 选项传入，详见 [Add Environment variables to your Addon](https://github.com/alexbelgium/hassio-addons/wiki/Add-Environment-variables-to-your-Addon-2)。

## 使用 / 访问入口

- 本加载项未启用 ingress（`ingress_port: 0`），需通过端口直接访问：Web 界面为 HTTPS，默认 `443` 端口映射到宿主机 `8099` 端口。
- 首次访问 `https://<HA主机IP>:8099`，在向导中创建管理员用户名、密码，并选择数据库。
- 若检测到已运行的 MariaDB 加载项，启动日志会输出数据库连接信息（数据库用户、密码、数据库名 `nextcloud`、主机 `core-mariadb:3306`），可据此在首次配置时选用 MariaDB 作为后端数据库。
- Home Assistant 集成：可使用官方 [Nextcloud 集成](https://www.home-assistant.io/integrations/nextcloud/) 对接本实例。

## 常见问题

- **首次打开提示 SQLite 性能警告**：这是 Nextcloud 对 SQLite 的提示，建议生产环境改用 MariaDB。可参照上游 README 的步骤：先安装并启动 `mariadb` 加载项，再安装/重启本加载项并查看日志中的数据库连接信息，用这些凭据配置 MariaDB 后再回到 Web 界面完成安装。
- **挂载的本地磁盘没有写权限**：这是当前版本一个已知问题（[issue #2123](https://github.com/alexbelgium/hassio-addons/issues/2123)），升级后若仍遇到可关注上游修复。
- **每次启动权限检查都很慢**：数据目录较大时，启动时的权限检查（chown/chmod）可能耗时较长，可开启 `skip_permissions_check` 跳过，但需自行确保目录权限正确。

---
- 英文原版：[Home assistant add-on: Nextcloud](https://github.com/alexbelgium/hassio-addons/blob/master/nextcloud/README.md)
- 来源仓库：alexbelgium
