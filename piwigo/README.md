<!-- zh-guide -->
# Piwigo

## 简介

Piwigo 是一款面向 Web 的照片画廊软件，可以组织、管理并展示你的照片集，支持相册、标签、插件扩展等功能。本加载项基于 linuxserver.io 的 Piwigo Docker 镜像构建，让你在 Home Assistant 上轻松运行自己的照片画廊。

## 安装

1. 在 Home Assistant → 设置 → 加载项 → 商店，添加本商店仓库：
   - Gitee：https://gitee.com/zhqznc_10603234_123/ha-addon
   - GitHub：https://github.com/Treasoni/ha-addon-cn
2. 搜索 piwigo 并安装。

## 配置

Piwigo 的配置大多在 Web 界面中完成，加载项选项主要用于文件权限、时区与磁盘挂载。可配置选项如下：

| 配置键 | 类型 / 默认值 | 说明 |
| ------ | ------------- | ---- |
| `PUID` | 整数，默认 `0` | 文件权限的用户 ID |
| `PGID` | 整数，默认 `0` | 文件权限的用户组 ID |
| `TZ` | 字符串（可选） | 时区（如 `Europe/London`） |
| `localdisks` | 字符串（可选） | 需要挂载的本地磁盘（如 `sda1,sdb1,MYNAS`） |
| `networkdisks` | 字符串（可选） | 需要挂载的 SMB 共享（如 `//SERVER/SHARE`） |
| `cifsusername` | 字符串（可选） | 网络共享的 SMB 用户名 |
| `cifspassword` | 字符串（可选） | 网络共享的 SMB 密码 |
| `cifsdomain` | 字符串（可选） | 网络共享的 SMB 域 |
| `env_vars` | 列表（可选） | 附加环境变量列表，每项包含 `name`（变量名）与 `value`（变量值），用于向容器传入额外环境变量 |

## 使用 / 访问入口

启动后打开 Web 界面（端口 `80/tcp` 映射到宿主端口 `81`，访问 `http://homeassistant.local:81`）。首次安装建议按以下步骤设置：

1. 在 MySQL/MariaDB 服务器中为 Piwigo 创建专用的用户和数据库。
2. 在 Piwigo 的数据库设置页面中，使用 IP 地址而不是主机名填写数据库服务器。
3. 如需 HTTPS（端口 443），可编辑 `/config/piwigo/nginx/site-confs` 下的 nginx 配置。
4. 自签名证书位于 `/data/keys`，如有需要可替换为你自己的证书。
5. 邮件相关设置可在 `/config/piwigo` 下的配置文件中修改。

## 常见问题

- **为什么打不开相册？** Piwigo 依赖 MySQL/MariaDB 数据库，请先在数据库服务器中为 Piwigo 创建用户和数据库，并在设置页中正确填写。
- **数据库连接失败？** 在 Piwigo 的数据库设置页面中请使用 IP 地址而非主机名填写数据库服务器地址。
- **如何启用 HTTPS？** 编辑 `/config/piwigo/nginx/site-confs` 下的 nginx 配置启用 SSL，自签名证书位于 `/data/keys`，建议替换为正式证书。
- **需要挂载额外磁盘吗？** 可通过 `localdisks`（本地磁盘）和 `networkdisks`（SMB 共享）选项挂载照片目录，配合 `cifsusername`、`cifspassword`、`cifsdomain` 填写网络共享凭据。

---
- 英文原版：Home assistant add-on: Piwigo；链接 https://github.com/alexbelgium/hassio-addons/blob/master/piwigo/README.md
- 来源仓库：alexbelgium
