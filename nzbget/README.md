<!-- zh-guide -->
# Nzbget

## 简介

Nzbget 是一款 Usenet 下载器，使用 C++ 编写，专为追求最高下载速度而设计，同时占用极少的系统资源。它非常适合在 Home Assistant 上以极低的资源开销高速下载 Usenet 内容。本加载项基于 linuxserver/docker-nzbget 镜像构建。

## 安装

1. 在 Home Assistant → 设置 → 加载项 → 商店，添加本商店仓库：
   - Gitee：https://gitee.com/zhqznc_10603234_123/ha-addon
   - GitHub：https://github.com/Treasoni/ha-addon-cn
2. 搜索 nzbget 并安装。

## 配置

Nzbget 的大部分配置都可以在软件的 Web 界面中完成，这里的选项主要用于文件权限、时区与磁盘挂载。可配置选项如下：

| 配置键 | 类型 / 默认值 | 说明 |
| ------ | ------------- | ---- |
| `PGID` | 整数，默认 `0` | 文件权限的用户组 ID |
| `PUID` | 整数，默认 `0` | 文件权限的用户 ID |
| `TZ` | 字符串（可选） | 时区（如 `Europe/London`） |
| `localdisks` | 字符串（可选） | 需要挂载的本地磁盘（如 `sda1,sdb1,MYNAS`） |
| `networkdisks` | 字符串（可选） | 需要挂载的 SMB 共享（如 `//SERVER/SHARE`） |
| `cifsusername` | 字符串（可选） | 网络共享的 SMB 用户名 |
| `cifspassword` | 字符串（可选） | 网络共享的 SMB 密码 |
| `cifsdomain` | 字符串（可选） | 网络共享的 SMB 域 |
| `env_vars` | 列表（可选） | 附加环境变量列表，每项包含 `name`（变量名）与 `value`（变量值），用于向容器传入额外环境变量 |

## 使用 / 访问入口

启动后可在 Home Assistant 侧边栏看到 Nzbget 图标，点击进入。若需要直接访问，Web 界面端口 `6789/tcp` 映射到宿主端口 `6789`。默认登录凭据为：用户名 `nzbget`，密码 `tegbzn6789`，首次登录后请在界面中修改。

## 常见问题

- **下载任务无法开始？** 请先在 Web 界面的设置中添加你的 Usenet 服务器信息（主机、端口、账号与连接数），这是下载的前提。
- **需要挂载额外的本地磁盘或网络共享怎么办？** 使用 `localdisks`（本地磁盘）和 `networkdisks`（SMB 共享）选项，并可配合 `cifsusername`、`cifspassword`、`cifsdomain` 填写网络共享凭据。
- **如何传递自定义环境变量？** 使用 `env_vars` 选项，每项填写 `name` 与 `value`，加载项会将其注入容器环境。
- **配置文件在哪里？** 配置文件位于加载项配置目录（`/addon_configs/xxx-nzbget`），升级后会被保留。
- **为什么下载速度上不去？** Nzbget 对性能敏感，可检查 Usenet 提供商允许的连接数并适当调整，同时确认下载目录所在磁盘的读写性能。

---
- 英文原版：Home assistant add-on: nzbget；链接 https://github.com/alexbelgium/hassio-addons/blob/master/nzbget/README.md
- 来源仓库：alexbelgium
