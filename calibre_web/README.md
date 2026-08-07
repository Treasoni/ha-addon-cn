<!-- zh-guide -->
# Calibre-web

## 简介
Calibre-web 是一个基于现有 Calibre 数据库的网页应用，提供简洁的界面用于浏览、阅读和下载电子书。它还支持集成 Google Drive，并可直接在应用内编辑元数据和你的 Calibre 图书馆。本加载项基于 linuxserver/docker-calibre-web 镜像构建。

## 安装
1. 在 Home Assistant → 设置 → 加载项 → 商店，添加本商店仓库：
   - Gitee：https://gitee.com/zhqznc_10603234_123/homeassistant
   - GitHub：https://github.com/Treasoni/ha-addon-cn
2. 搜索 calibre_web 并安装。

## 配置
大部分配置可通过应用的 Web 界面完成，只有以下选项需要在加载项配置中设置。

| 配置键 | 类型/默认值 | 说明 |
|--------|-------------|------|
| `PGID` | int / `0` | 文件权限的组 ID |
| `PUID` | int / `0` | 文件权限的用户 ID |
| `TZ` | str / 空 | 时区，例如 `Asia/Shanghai` |
| `DOCKER_MODS` | str / 空 | 要应用的 Docker 修改（镜像默认已内置 `linuxserver/mods:universal-calibre`） |
| `OAUTHLIB_RELAX_TOKEN_SCOPE` | str / 空 | 放宽 OAuth token 作用域校验 |
| `ingress_user` | str / 空 | Ingress 认证使用的用户名 |
| `localdisks` | str / 空 | 要挂载的本地磁盘，例如 `sda1,sdb1,MYNAS` |
| `networkdisks` | str / 空 | 要挂载的 SMB 远程共享，例如 `//SERVER/SHARE` |
| `cifsusername` | str / 空 | SMB 共享的用户名 |
| `cifspassword` | str / 空 | SMB 共享的密码 |
| `cifsdomain` | str / 空 | SMB 共享的域 |
| `env_vars` | list / `[]` | 额外环境变量，每项为 name/value 键值对 |

挂载本地磁盘与 SMB 远程共享的详细说明，参见 alexbelgium wiki 中的 "Mounting Local Drives in Addons" 与 "Mounting Remote Shares in Addons"。

## 使用 / 访问入口
- **Ingress（推荐）**：通过 Home Assistant 侧边栏直接打开，无需额外端口。
- **端口访问**：加载项容器内监听 `8083` 端口，映射到宿主机 `8084` 端口（http://homeassistant:8084）。使用 Ingress 时无需该端口。
- **首次访问**：默认账号为 `admin`，默认密码 `admin123`（启动日志中也会打印）。
- 首次登录后按提示指定 Calibre 数据库路径，即可浏览、阅读、下载电子书，并编辑元数据。

## 常见问题
1. 下载图书报 500 错误？该问题已在 0.6.26-2 版本修复——镜像在构建时即安装 calibredb。
2. 配置数据在哪里？新版配置已迁移到 `/addon_configs/<slug>-calibre-web` 目录（可通过 Filebrowser 加载项访问），旧版位于 `/config/hassio_addons/calibre-web`，迁移会自动完成，注意更新相关链接。
3. 首次启动 Ingress 可能暂不可用，重启一次加载项即可启用自动登录。

---
- 英文原版：Home assistant add-on: Calibre-web；链接 https://github.com/alexbelgium/hassio-addons/blob/master/calibre_web/README.md
- 来源仓库：alexbelgium
