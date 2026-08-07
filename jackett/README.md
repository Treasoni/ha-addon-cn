<!-- zh-guide -->
# Jackett NAS

## 简介

Jackett NAS 是一个索引器（indexer）代理工具：它把 Sonarr、SickRage、CouchPotato、Mylar 等媒体应用发来的查询请求，转换为各个 PT 站/tracker 站点专用的 HTTP 查询，解析返回的 HTML 页面后，把命中结果回传给发起请求的软件。本加载项基于 linuxserver.io 的 docker-jackett 镜像构建。

## 安装

1. 在 Home Assistant → 设置 → 加载项 → 商店，添加本商店仓库：
   - Gitee：https://gitee.com/zhqznc_10603234_123/homeassistant
   - GitHub：https://github.com/Treasoni/ha-addon-cn
2. 搜索 jackett 并安装。

## 配置

以下配置键可在加载项配置界面中设置：

| 配置键 | 类型/默认值 | 说明 |
|--------|-------------|------|
| `PGID` | int / `0` | 文件权限的组 ID |
| `PUID` | int / `0` | 文件权限的用户 ID |
| `TZ` | str / 空 | 时区，例如 `Europe/London` |
| `localdisks` | str / 空 | 要挂载的本地磁盘，多个用逗号分隔（例如 `sda1,sdb1,MYNAS`） |
| `networkdisks` | str / 空 | 要挂载的 SMB 网络共享（例如 `//192.168.1.100/downloads`） |
| `cifsusername` | str / 空 | 网络共享的 SMB 用户名 |
| `cifspassword` | str / 空 | 网络共享的 SMB 密码 |
| `cifsdomain` | str / 空 | 网络共享的 SMB 域（工作组） |
| `env_vars` | 数组 / `[]` | 追加额外的环境变量（`name`/`value` 列表，变量名需匹配 `^[A-Za-z0-9_]+$`） |

> 除上述选项外，其余配置均可通过 Jackett 的 Web 界面完成。

### 挂载磁盘

- **本地磁盘**：在 `localdisks` 中填写设备名或卷标（如 `sda1`、`MYNAS`）。
- **远程 SMB 共享**：在 `networkdisks` 中填写 `//服务器/共享路径`，并配合 `cifsusername`、`cifspassword`、`cifsdomain` 填写访问凭据。

## 使用 / 访问入口

- **Web 界面端口**：`9117`（Web 界面），备用端口 `8889`。首次访问地址为 `http://<主机地址>:9117`。
- 也可通过 Home Assistant 侧边栏的加载项入口访问 Web 界面。
- 配置数据保存在 `/config/addons_config/Jackett`；首次启动时若检测到旧版目录 `/config/Jackett`，会自动迁移到新位置。同时会自动创建 `/share/downloads` 作为默认下载目录。

## 常见问题

- **修改 `localdisks` / `networkdisks` 后没有生效？** 确认填写的设备名/卷标（本地磁盘）或共享路径与访问凭据（SMB）正确，然后重启加载项使挂载生效。
- **找不到配置目录？** Jackett 的配置位于 `/config/addons_config/Jackett`，早期版本的 `/config/Jackett` 会在首次启动时自动迁移。
- **访问不了 Web 界面？** 确认加载项已启动且日志正常，检查 `http://<主机地址>:9117` 端口是否可访问。

---
- 英文原版：Home assistant add-on: jackett，链接 https://github.com/alexbelgium/hassio-addons/blob/master/jackett/README.md
- 来源仓库：alexbelgium
