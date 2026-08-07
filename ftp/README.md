<!-- zh-guide -->
# FTP

## 简介

FTP 协议虽然古老，但在某些场景下仍然很有用，例如大多数 IP 摄像头仍支持通过 FTP 上传图片或视频。本加载项以较为安全的方式为 Home Assistant 提供一个 FTP 服务器：虽然 FTP 本身基于明文传输并不完全安全，但本加载项支持 FTP over SSL（FTPS），并将虚拟用户限制（chroot）在其主目录中。当然，如果你愿意，也可以用它通过 FTP 访问 Home Assistant 的配置。

## 安装

1. 在 Home Assistant → 设置 → 加载项 → 商店，添加本商店仓库：
   - Gitee：https://gitee.com/zhqznc_10603234_123/ha-addon
   - GitHub：https://github.com/Treasoni/ha-addon-cn
2. 搜索 ftp 并安装。

## 配置

在加载项“配置”页修改配置后，需要重启加载项才能生效。可选配置键如下：

| 配置键 | 类型/默认值 | 说明 |
| ------ | ----------- | ---- |
| `log_level` | 可选 `list(trace|debug|info|notice|warning|error|fatal)`，默认 `info` | 日志输出详细程度：`trace` 输出全部细节；`debug` 输出调试信息；`info` 常规事件；`warning` 非错误的异常事件；`error` 运行时错误；`fatal` 致命错误。更高级别会自动包含更低级别的日志，同样影响 FTP 服务器的日志级别 |
| `port` | 端口，默认 `21` | FTP 监听传入连接使用的端口 |
| `data_port` | 端口，默认 `20` | PORT 主动模式数据连接使用的源端口 |
| `banner` | `str`，默认 `Welcome to the Hass.io FTP service.` | FTP 服务器在连接建立时显示的欢迎横幅 |
| `pasv` | `bool`，默认 `true` | 是否允许使用 PASV 被动模式建立数据连接，设为 `false` 则禁用 |
| `pasv_min_port` | 端口，默认 `30000` | 被动模式数据连接分配的最小端口，可用于缩小端口范围以便配合防火墙 |
| `pasv_max_port` | 端口，默认 `30010` | 被动模式数据连接分配的最大端口 |
| `pasv_address` | `str`，默认 `空` | 覆盖 PASV 响应中通告的 IP 地址，可填数字 IP 或主机名（启动时解析）；留空则取自有连接的套接字 |
| `pasv_addr_resolve` | 可选 `bool`，默认 `空` | 设为 `true` 允许在 PASV 连接中解析主机名 |
| `ssl` | `bool`，默认 `false` | 是否在 FTP 服务器上启用 SSL（FTPS），设为 `true` 启用 |
| `certfile` | `str`，默认 `fullchain.pem` | 用于 SSL 的证书文件，必须存放在 `/ssl/` 目录 |
| `keyfile` | `str`，默认 `privkey.pem` | 用于 SSL 的私钥文件，必须存放在 `/ssl/` 目录 |
| `implicit_ssl` | `bool`，默认 `false` | 设为 `true` 时，所有连接上首先进行 SSL 握手（FTPS 协议） |
| `max_clients` | `int`，默认 `5` | 同一时间允许连接的最大客户端数，超出的客户端会收到错误提示 |
| `users` | 列表/对象列表（含 `username`、`password` 等子键），默认 `空` | 一个或多个用户的列表，每个用户可有各自独立的权限（见下方子键） |
| `users.username` | `str`，默认 `hassio` | 用户登录 FTP 服务器使用的用户名，最多 32 个字符，仅含 `A-Z` 与 `0-9`，可含连字符（`-`）但不能以连字符开头或结尾 |
| `users.password` | `str`（密码），默认 `changeme` | 该用户登录使用的密码 |
| `users.allow_chmod` | `bool`，默认 `false` | 设为 `true` 允许该用户使用 `SITE CHMOD` 命令 |
| `users.allow_download` | `bool`，默认 `false` | 设为 `true` 允许该用户从 FTP 服务器下载文件 |
| `users.allow_upload` | `bool`，默认 `false` | 是否允许任何修改文件系统的 FTP 命令（如 `STOR`、`DELE`、`RNFR`、`RNTO`、`MKD`、`RMD`、`APPE`、`SITE`） |
| `users.allow_dirlist` | `bool`，默认 `true` | 设为 `true` 允许用户使用列表命令浏览其有权限访问的目录 |
| `users.addons` | `bool`，默认 `false` | 允许该用户访问 `/addons` 目录 |
| `users.backup` | `bool`，默认 `false` | 允许该用户访问 `/backup` 目录 |
| `users.config` | `bool`，默认 `false` | 允许该用户访问 `/config` 目录 |
| `users.media` | `bool`，默认 `true` | 允许该用户访问 `/media` 目录 |
| `users.share` | `bool`，默认 `true` | 允许该用户访问 `/share` 目录 |
| `users.ssl` | `bool`，默认 `false` | 允许该用户访问 `/ssl` 目录 |
| `i_like_to_be_pwned` | 可选 `bool`，默认 `空` | 设为 `true` 可绕过 HaveIBeenPwned 的强密码要求。强烈建议改用更安全的长密码，而不是使用此选项，风险自负 |

## 使用 / 访问入口

- **连接方式**：加载项使用 host 网络模式运行，FTP 服务器默认监听宿主机端口 21。使用任意 FTP 客户端，以你的 Home Assistant 设备 IP 作为地址、端口 21 进行连接即可。
- **默认账号**：默认配置了一个用户 `hassio`（密码 `changeme`），可访问 `/media` 与 `/share` 目录。建议登录后立即在配置中修改密码并调整目录权限。
- **被动模式**：若 FTP 客户端使用被动（PASV）模式，数据连接端口范围为 30000 至 30010，如需配置防火墙请放行该范围。
- **启用 FTPS**：如需加密传输，将 `ssl` 设为 `true` 并配置证书，客户端以 FTPS 方式连接。

## 常见问题

- **默认密码是什么？** 默认用户为 `hassio`，密码为 `changeme`。出于安全考虑，请务必修改为强密码，除非你真的清楚使用 `i_like_to_be_pwned` 的后果。
- **摄像头如何上传？** 将 `users.allow_upload` 设为 `true`，并为该用户开放对应的目录权限（如 `/media`、`/share`），然后在摄像头中填写 FTP 服务器地址、用户名与密码即可。
- **为什么无法用被动模式连接？** 请确认防火墙放行了 30000 至 30010 的被动端口范围，且 `pasv` 未被设为 `false`。
- **FTP 是否安全？** FTP 本身为明文传输，建议启用 `ssl`（FTPS）以加密传输；此外加载项会将每个虚拟用户限制（chroot）在其主目录内。

---
- 英文原版：Home Assistant Community Add-on: FTP；链接 https://github.com/hassio-addons/repository/blob/main/ftp/README.md
- 来源仓库：frenck
