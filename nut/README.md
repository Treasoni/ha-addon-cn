<!-- zh-guide -->
# Network UPS Tools

## 简介

Network UPS Tools（NUT）是一个运行在 Home Assistant 机器上的 UPS 守护进程，用于轻松管理连接到你设备的电池后备电源（UPS）。NUT 项目的核心目标是支持各类电源设备，如不间断电源（UPS）、电源分配单元（PDU）、自动转换开关（ATS）、电源供应单元和太阳能控制器，并提供统一的控制与监控接口。已有超过 140 家厂商的数千款型号与 NUT 兼容。

启动本应用后，请在 Home Assistant 中添加 NUT 集成，即可在界面中监控 UPS 状态。

## 安装

1. 在 Home Assistant 中进入「设置 → 加载项 → 商店」，点击右上角菜单添加本商店仓库：
   - Gitee：https://gitee.com/zhqznc_10603234_123/ha-addon
   - GitHub：https://github.com/Treasoni/ha-addon-cn
2. 在商店中搜索 `nut`（Network UPS Tools）并点击安装。
3. 按下方说明配置 `users` 和 `devices` 选项，然后启动应用。
4. 查看应用日志确认一切正常，并记录「信息」标签页中的主机名。
5. 在 Home Assistant 中添加 NUT 集成，使用记录的主机名、端口 `3493` 以及应用内配置的用户名/密码完成连接。

## 配置

> 注意：修改配置后需重启应用才会生效。

| 配置键 | 类型 / 默认值 | 说明 |
| --- | --- | --- |
| `log_level` | 枚举（trace\|debug\|info\|notice\|warning\|error\|fatal），可选 / 空 | 应用的日志输出级别。`trace` 显示全部细节，`debug` 显示详细调试信息，`info` 为正常事件，`warning` 为非错误的异常，`error` 为无需立即处理的错误，`fatal` 为致命错误。推荐使用 `info`。 |
| `users` | 列表（对象列表） / 空（默认一个空凭据用户） | 允许访问 NUT 服务器的用户列表，可为每个用户单独设置权限。 |
| `users.username` | 字符串 / 空 | 用户登录 NUT 服务器的用户名。有效字符仅包含 `a-z`、`A-Z`、`0-9` 和下划线（`_`）。 |
| `users.password` | 密码 / 空 | 该用户的密码。 |
| `users.instcmds` | 字符串列表 / [all] | 允许该用户执行的即时命令列表，填入 `all` 表示授权所有命令。 |
| `users.actions` | 字符串列表 / 空 | 允许该用户执行的操作列表，可选值为 `set`（修改 UPS 变量）和 `fsd`（强制关闭标志，等效于「电池供电 + 低电量」）。 |
| `users.upsmon` | 枚举（primary\|secondary\|master\|slave），可选 / 空 | 是否为 upsmon 进程添加所需操作。`netclient` 方式的从机账号应设为 `secondary`。 |
| `devices` | 列表（对象列表） / 空（默认一项 `myups`） | 连接到本机的 UPS 设备列表。 |
| `devices.name` | 字符串 / myups | UPS 名称，不能包含空格，也不能命名为 `default`。 |
| `devices.driver` | 字符串 / usbhid-ups | 监控该 UPS 所使用的驱动程序，需选择与硬件兼容的驱动。 |
| `devices.port` | 字符串 / auto | UPS 连接的串口，通常第一个串口为 `/dev/ttyS0`，使用 `auto` 可自动检测端口。 |
| `devices.powervalue` | 整数，可选 / 空 | 该 UPS 是否为当前主机供电：`1` 表示为主机供电，`0` 表示仅监控。至少需要一个 `powervalue` 为 `1` 的设备。 |
| `devices.config` | 字符串列表 / 空 | 该 UPS 的附加配置项列表，例如使用 `vendorid`、`product`、`serial` 等区分多个 USB 设备。 |
| `mode` | 枚举（netserver\|netclient）/ netserver | `netserver` 运行管理本地 UPS 所需的组件并允许客户端连接；`netclient` 仅运行 `upsmon` 连接远程 `netserver`。 |
| `shutdown_host` | 布尔 / false | 设为 `true` 时，UPS 关机命令会一并关闭宿主机；设为 `false` 时仅停止本应用，便于无影响的测试。 |
| `list_usb_devices` | 布尔，可选 / 空 | 设为 `true` 时，启动日志会列出已连接的 USB 设备，便于在多个 UPS 时识别设备。 |
| `remote_ups_name` | 字符串，可选 / 空 | `netclient` 模式下远程 UPS 的名称。 |
| `remote_ups_host` | 字符串，可选 / 空 | `netclient` 模式下远程 UPS 的主机。 |
| `remote_ups_user` | 字符串，可选 / 空 | `netclient` 模式下远程 UPS 的用户。 |
| `remote_ups_password` | 密码，可选 / 空 | `netclient` 模式下远程 UPS 的密码。使用远程选项时，`users` 和 `devices` 仍需保留但不会生效。 |
| `upsd_maxage` | 整数，可选 / 空 | 设置 upsd.conf 中的 MAXAGE 值，用于增大特定驱动的超时时间，多数用户无需修改。 |
| `upsmon_deadtime` | 整数，可选 / 空 | 设置 upsmon.conf 中的 DEADTIME 值，用于调整监控进程的过期时间，多数用户无需修改。 |
| `i_like_to_be_pwned` | 布尔，可选 / 空 | 设为 `true` 可绕过 HaveIBeenPwned 的密码强度要求。强烈建议设置更强的安全密码而不是使用此选项，风险自负。 |
| `leave_front_door_open` | 布尔，可选 / 空 | 设为 `true` 并留空用户名和密码可禁用 NUT 服务器认证。强烈建议不要使用，即使仅暴露在内网，风险自负。 |

## 使用 / 访问入口

本应用不提供 Web 界面，而是以 NUT 服务运行在端口 `3493/tcp`（默认未映射固定宿主端口）。请在 Home Assistant 中添加 NUT 集成，填入应用信息标签页中的主机名、端口 `3493` 以及你配置的用户名/密码。

## 常见问题

- **设备无法被发现**：请确认 `devices` 中至少有一个设备设置了 `powervalue: 1`，且驱动与硬件兼容；多个 USB 设备时可在 `devices.config` 中用 `vendorid`/`product` 区分。
- **NUT 集成连不上**：检查 `users` 中配置的用户名/密码，并使用信息页中的主机名与端口 `3493` 连接。
- **`shutdown_host` 的作用**：`false`（默认）时 UPS 关机命令只停止应用不影响系统，便于测试；确认无误后再设为 `true`。
- **测试密码强度提示**：若 NUT 集成提示密码过弱，请改用更强密码，而非开启 `i_like_to_be_pwned`。
- **UPS 状态自动化**：UPS 状态变化时会触发 `nut.ups_event` 事件，可用于创建通知自动化。
- **主备术语**：`upsmon` 建议使用 `primary`/`secondary`（master/slave 已弃用）。

---
- 英文原版：Network UPS Tools；链接 https://github.com/hassio-addons/repository/blob/main/nut/README.md
- 来源仓库：frenck
