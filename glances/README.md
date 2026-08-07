<!-- zh-guide -->
# Glances

## 简介

Glances 是一款跨平台的系统监控工具，旨在通过基于 Web 的界面，在尽可能小的空间中呈现尽可能多的系统信息。它可以将所有系统统计信息导出到 InfluxDB，方便你查看系统信息及其随时间变化的行为。通过本加载项，你可以在 Home Assistant 中直接监控设备的 CPU、内存、磁盘、网络等运行状态。

## 安装

1. 在 Home Assistant → 设置 → 加载项 → 商店，添加本商店仓库：
   - Gitee：https://gitee.com/zhqznc_10603234_123/ha-addon
   - GitHub：https://github.com/Treasoni/ha-addon-cn
2. 搜索 glances 并安装。

## 配置

在加载项“配置”页修改配置后，需要重启加载项才能生效。可选配置键如下：

| 配置键 | 类型/默认值 | 说明 |
| ------ | ----------- | ---- |
| `log_level` | `list(trace|debug|info|notice|warning|error|fatal)`，默认 `info` | 日志输出详细程度：`trace` 输出全部细节；`debug` 输出调试信息；`info` 常规事件；`warning` 非错误的异常事件；`error` 运行时错误；`fatal` 致命错误。更高级别会自动包含更低级别的日志，默认 `info` 是推荐设置 |
| `process_info` | `bool`，默认 `false` | 设为 `true` 启用 Glances 的进程模块，可查看系统上每个进程的详细信息；启用会显著增加 CPU 占用 |
| `refresh_time` | `int`，默认 `10` | 界面刷新间隔（秒）；刷新越快 CPU 占用越高 |
| `ssl` | `bool`，默认 `false` | 是否在 Glances Web 界面启用 SSL（HTTPS），设为 `true` 启用 |
| `certfile` | `str`，默认 `fullchain.pem` | 用于 SSL 的证书文件，必须存放在 `/ssl/` 目录 |
| `keyfile` | `str`，默认 `privkey.pem` | 用于 SSL 的私钥文件，必须存放在 `/ssl/` 目录 |
| `influxdb` | 对象/嵌套配置，默认 `空` | Glances 向 InfluxDB 导出数据的相关配置（见下方子键） |
| `influxdb.enabled` | `bool`，默认 `false` | 是否启用向 InfluxDB 导出 Glances 数据 |
| `influxdb.host` | `str`，默认 `a0d7b954-influxdb` | InfluxDB 运行的主机名；若使用社区 InfluxDB 加载项，请填 `a0d7b954-influxdb` |
| `influxdb.port` | 端口，默认 `8086` | InfluxDB 监听的端口 |
| `influxdb.interval` | `int`，默认 `60` | 向 InfluxDB 导出数据的间隔（秒） |
| `influxdb.ssl` | `bool`，默认 `false` | 是否在 InfluxDB 连接上使用 SSL；社区 InfluxDB 加载项要求设为 `false` |
| `influxdb.prefix` | `str`，默认 `localhost` | 附加到导出数据上的主机名前缀；使用 Grafana Glances 仪表盘时请设为 `localhost` |
| `influxdb.version` | `int`，默认 `1` | 要连接的 InfluxDB 版本，取 `1` 或 `2` |
| `influxdb.username` | `str`，默认 `glances` | 仅 v1 生效：为 Glances 创建的认证用户名 |
| `influxdb.password` | `str`（密码），默认 `空` | 仅 v1 生效：上述用户名的密码 |
| `influxdb.database` | `str`，默认 `glances` | 仅 v1 生效：存储 Glances 数据的数据库名；强烈建议为 Glances 单独建库，不要与 Home Assistant 共用 |
| `influxdb.token` | `str`，默认 `空` | 仅 v2 生效：具有指定桶写入权限的 InfluxDB token |
| `influxdb.bucket` | `str`，默认 `空` | 仅 v2 生效：存储 Glances 数据的桶名；建议单独建桶，不要与 Home Assistant 共用 |
| `influxdb.org` | `str`，默认 `空` | 仅 v2 生效：拥有该桶的 InfluxDB 组织名 |
| `leave_front_door_open` | `bool`，默认 `false` | 设为 `true` 将禁用 Glances Web 界面的登录认证。**强烈不建议启用**，风险自负 |

## 使用 / 访问入口

- **Web 界面**：加载项支持 Ingress，启动后可在 Home Assistant 侧边栏看到 Glances 图标，点击进入即可查看系统监控信息。
- **直接访问（可选）**：端口 `80/tcp` 为 Web 界面直连端口（Ingress 场景下无需使用），仅在需要绕过 Ingress 直接访问时才会用到。
- **作为 Home Assistant 传感器**：在 Home Assistant 中通过 **设置 → 设备与服务 → 集成 → 添加集成 → Glances** 添加，即可将系统统计作为传感器展示，并可用于构建自动化。添加时除端口外使用默认设置（端口改为 61209）。

## 常见问题

- **InfluxDB 数据导不出来？** 请确认 `influxdb.host` 填写正确（社区 InfluxDB 加载项用 `a0d7b954-influxdb`）、`influxdb.port` 与数据库实际端口一致，且 `influxdb.ssl` 对社区加载项必须为 `false`。
- **如何让 Grafana 仪表盘正常显示？** 将 `influxdb.prefix` 设为 `localhost`，即可匹配 Grafana Glances 仪表盘的数据前缀。
- **监控很耗 CPU？** 启用 `process_info` 或过快的 `refresh_time` 都会显著增加 CPU 占用，请按需调整。
- **密码没生效？** 若使用 InfluxDB v2，`username` 与 `password` 不生效，应使用 `token` 与 `bucket`；v1 则对应 `username`、`password` 与 `database`。

---
- 英文原版：Home Assistant Community App: Glances；链接 https://github.com/hassio-addons/repository/blob/main/glances/README.md
- 来源仓库：frenck
