<!-- zh-guide -->
# Unpackerr

## 简介

Unpackerr 以守护进程方式运行在下载主机上，检测下载客户端已完成的任务并自动解压，使 Lidarr、Radarr、Readarr、Sonarr 等 *arr 应用能够导入这些文件。本加载项基于 hotio/unpackerr 镜像构建。

## 安装

1. 在 Home Assistant → 设置 → 加载项 → 商店，添加本商店仓库：
   - Gitee：https://gitee.com/zhqznc_10603234_123/ha-addon
   - GitHub：https://github.com/Treasoni/ha-addon-cn
2. 搜索 unpackerr 并安装。

## 配置

修改配置后需要重启加载项才能生效。可选配置键如下：

| 配置键 | 类型/默认值 | 说明 |
| ------ | ----------- | ---- |
| `env_vars` | 列表，默认空 | 传入容器的自定义环境变量列表，每项包含 `name`（变量名，须匹配 `^[A-Za-z0-9_]+$`）与 `value`（变量值，可选）。 |
| `PGID` | 整数，默认 `1000` | 文件权限使用的组 ID。 |
| `PUID` | 整数，默认 `1000` | 文件权限使用的用户 ID。 |
| `TZ` | 可选字符串，默认空 | 时区，例如 `Europe/London`。 |
| `extraction_path` | 字符串，默认 `/share/downloads_packed` | 下载客户端存放已下载压缩包的目录。 |
| `watch_path` | 字符串，默认 `/share/downloads_unpacked` | 解压后文件存放的目录，供 *arr 应用监视导入。 |
| `cifsdomain` | 可选字符串，默认空 | 网络共享（SMB）的域/工作组。 |
| `cifspassword` | 可选字符串，默认空 | 网络共享（SMB）的密码。 |
| `cifsusername` | 可选字符串，默认空 | 网络共享（SMB）的用户名。 |
| `localdisks` | 可选字符串，默认空 | 需要挂载的本地磁盘，例如 `sda1,sdb1`。 |
| `networkdisks` | 可选字符串，默认空 | 需要挂载的 SMB 网络共享，例如 `//SERVER/SHARE`。 |

## 使用 / 访问入口

本加载项没有 Web 界面，也没有对外端口，它作为后台服务自动运行。使用步骤如下：

1. 将下载客户端配置为把已完成的下载保存到 `extraction_path` 目录。
2. 确认解压后的文件会输出到 `watch_path` 目录。
3. 在 Sonarr / Radarr / Lidarr 等应用中配置监视 `watch_path` 目录以便自动导入。
4. 启动加载项，通过「日志」观察解压活动是否正常。

## 常见问题

- **如何修改高级配置？** 自 0.12.0 起配置迁移到 `/addon_configs/db21ed7f_unpackerr/unpackerr.conf`（可通过 Filebrowser 加载项访问）。可在该文件中按上游 Unpackerr 的环境变量列表自行设置全部选项。
- **注意 `PUID`/`PGID` 权限。** 应用不允许以 root 运行，请确保 `PUID`/`PGID` 与实际文件权限对应，否则可能无法读取或写入下载目录。
- **`extraction_path`/`watch_path` 选项已弃用？** 从 0.12.0-3 起这两个选项已弃用，改动需要在 `unpackerr.conf` 中手动进行，以免破坏配置文件。
- **环境变量没有生效？** 自 v0.15.2-2 起修复了环境变量（如 `VPN_ENABLED`、`VPN_AUTO_PORT_FORWARD`）未传入容器的问题；当未配置 VPN 提供商时，VPN 端口转发服务会自动停用。
- 自 v0.15.0 起新增 `env_vars` 选项用于传入自定义环境变量；可参考上游 wiki「Running custom scripts in Addons」运行自定义脚本。
- 如何挂载本地磁盘或远程共享，参见上游 wiki「Mounting Local Drives in Addons」与「Mounting Remote Shares in Addons」。

---
- 英文原版：Home assistant add-on: Unpackerr；链接 https://github.com/alexbelgium/hassio-addons/blob/master/unpackerr/README.md
- 来源仓库：alexbelgium
