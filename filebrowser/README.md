<!-- zh-guide -->
# Filebrowser

## 简介
Filebrowser 是一个基于 Web 的文件管理界面，用于在指定目录内浏览、上传、删除、预览、重命名和编辑文件。它基于官方 [filebrowser/filebrowser](https://hub.docker.com/r/filebrowser/filebrowser) 镜像构建，界面简洁现代，支持多种文件格式预览与完整的文件操作，可作为 Home Assistant 的可视化文件管理器使用。

## 安装
1. 在 Home Assistant → 设置 → 加载项 → 商店，添加本商店仓库：
   - Gitee：https://gitee.com/zhqznc_10603234_123/homeassistant
   - GitHub：https://github.com/Treasoni/ha-addon-cn
2. 搜索 filebrowser 并安装。
3. 点击「保存」存储配置，然后启动加载项，查看日志确认运行正常。

## 配置
以下选项可在加载项「配置」页中设置：

| 配置键 | 类型/默认值 | 说明 |
|--------|-------------|------|
| `ssl` | bool / `false` | 为 Web 界面启用 HTTPS |
| `certfile` | str / `fullchain.pem` | SSL 证书文件（位于 `/ssl/` 目录） |
| `keyfile` | str / `privkey.pem` | SSL 私钥文件（位于 `/ssl/` 目录） |
| `NoAuth` | bool / `true` | 关闭登录认证（切换此选项会重置数据库） |
| `base_folder` | str / 可选 | 文件浏览器根目录；不填则默认显示所有映射的文件夹 |
| `disable_thumbnails` | bool / `true` | 关闭缩略图生成以提升性能 |
| `follow_external_symlinks` | bool / `true` | 是否跟踪外部符号链接 |
| `localdisks` | str / 可选 | 要挂载的本地硬盘，如 `sda1,sdb1,MYNAS`（用逗号分隔） |
| `networkdisks` | str / 可选 | 要挂载的 SMB 网络共享，如 `//SERVER/SHARE` |
| `cifsusername` | str / 可选 | SMB 共享用户名 |
| `cifspassword` | str / 可选 | SMB 共享密码 |
| `cifsdomain` | str / 可选 | SMB 共享域 |
| `env_vars` | 数组 / `[]` | 追加自定义环境变量（键名需匹配 `^[A-Za-z0-9_]+$`） |

## 使用 / 访问入口
- **侧边栏访问**：通过 Home Assistant 侧边栏入口（Ingress）直接打开，无需额外端口。
- **直接访问**：也可在浏览器访问 `http://<你的HA地址>:8071`（该端口为 Web UI 端口）。
- **首次登录**：默认账号 `admin` / 密码 `admin`；若开启了 `NoAuth` 选项，则跳过登录直接进入。
- **修改密码**：登录后建议立即点击「设置」→「用户管理」修改默认密码，保障安全。
- **常用操作**：上传、下载、删除、预览、重命名、编辑文件；支持本地硬盘与 SMB 网络共享挂载。

## 常见问题
- **为什么改了 NoAuth 后账号全没了？** 切换认证方式会重置 filebrowser 数据库，所有用户和设置被清空，账号恢复为默认的 `admin`/`admin`，属正常行为。
- **开启 ssl 后界面打不开？** 请检查证书路径是否正确，或暂时关闭 `ssl` 选项；证书需放置在 `/ssl/` 目录。
- **挂载本地硬盘 / SMB 共享**：本地硬盘与远程共享分别通过 `localdisks` 和 `networkdisks` 配置，具体请参考作者 Wiki（[本地硬盘挂载](https://github.com/alexbelgium/hassio-addons/wiki/Mounting-Local-Drives-in-Addons)、[远程共享挂载](https://github.com/alexbelgium/hassio-addons/wiki/Mounting-remote-shares-in-Addons)）。

---
- 英文原版：[Home assistant add-on: Filebrowser](https://github.com/alexbelgium/hassio-addons/blob/master/filebrowser/README.md)
- 来源仓库：alexbelgium
