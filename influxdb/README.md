<!-- zh-guide -->
# InfluxDB

## 简介

InfluxDB 是一款针对高写入量场景优化的开源时序数据库，适合记录指标、传感器数据、事件并进行分析。它对外提供 HTTP API 供客户端交互，常与 Grafana 搭配用于数据可视化。本加载项还预装了 Chronograf 与 Kapacitor，提供便捷的 InfluxDB 管理界面，用于管理用户、数据库、数据保留策略，并通过 Data Explorer 查看数据库内部数据。

## 安装

1. 在 Home Assistant → 设置 → 加载项 → 商店，添加本商店仓库：
   - Gitee：https://gitee.com/zhqznc_10603234_123/ha-addon
   - GitHub：https://github.com/Treasoni/ha-addon-cn
2. 搜索 influxdb 并安装。

## 配置

在加载项“配置”页修改配置后，需要重启加载项才能生效。可选配置键如下：

| 配置键 | 类型/默认值 | 说明 |
| ------ | ----------- | ---- |
| `log_level` | 可选 `list(trace|debug|info|notice|warning|error|fatal)`，默认 `info` | 日志输出详细程度：`trace` 输出全部细节；`debug` 输出调试信息；`info` 常规事件；`warning` 非错误的异常事件；`error` 运行时错误；`fatal` 致命错误。更高级别会自动包含更低级别的日志，默认 `info` 是推荐设置 |
| `auth` | `bool`，默认 `true` | 启用或禁用 InfluxDB 用户认证。**不建议关闭** |
| `reporting` | `bool`，默认 `true` | 是否向 InfluxData 上报使用数据；**不会传输任何用户数据库中的数据** |
| `ssl` | `bool`，默认 `true` | 是否在 Web 界面上启用 SSL（HTTPS）。注意：此选项**只作用于 Web 界面**，不会为 InfluxDB 服务本身启用 SSL |
| `certfile` | `str`，默认 `fullchain.pem` | 用于 SSL 的证书文件，必须存放在 `/ssl/` 目录 |
| `keyfile` | `str`，默认 `privkey.pem` | 用于 SSL 的私钥文件，必须存放在 `/ssl/` 目录 |
| `envvars` | 列表/对象列表（含 `name`、`value` 子键），默认 `空` | 通过环境变量控制 InfluxDB 配置（详见 InfluxDB 官方配置文档）；修改可能引发问题，风险自负，变量名区分大小写 |
| `envvars.name` | `str`，默认 `空` | 要设置的环境变量名，必须以 `INFLUXDB_` 开头 |
| `envvars.value` | `str`，默认 `空` | 要设置的环境变量值，请始终以字符串形式填写（包括 true/false 值） |
| `leave_front_door_open` | 可选 `bool`，默认 `空` | 设为 `true` 并留空用户名与密码，可禁用 Web 终端的认证。**强烈不建议使用**，即使加载项仅暴露在内网，风险自负 |

## 使用 / 访问入口

- **Web 界面**：加载项支持 Ingress，启动后可在 Home Assistant 侧边栏看到 InfluxDB 图标，点击进入（Chronograf 管理界面）。端口 `80/tcp` 为直连端口（Ingress 场景下无需使用）。
- **InfluxDB 服务**：端口 `8086/tcp` 映射到宿主机端口 8086，供客户端（如 Home Assistant 集成、Grafana 数据源）连接写入。
- **备份与恢复 RPC 服务**：端口 `8088/tcp` 映射到宿主机端口 8088，用于 InfluxDB 的备份与恢复。

## 常见问题

- **InfluxDB 服务支持 SSL 吗？** 目前加载项只支持 Web 界面的 SSL，InfluxDB 服务本身不支持 SSL，这是 Chronograf 带来的限制。
- **如何把 Home Assistant 数据写入 InfluxDB？** 在 Web 界面中创建数据库（如 `homeassistant`）和用户（如 `homeassistant`）并授予权限，然后在 Home Assistant 的 `configuration.yaml` 中添加 `influxdb` 集成，主机填 `a0d7b954-influxdb`、端口 `8086`、填入数据库、用户名与密码，重启 Home Assistant 即可。
- **关闭认证安全吗？** 关闭 `auth` 会禁用 InfluxDB 用户认证，任何人都可以读写数据，强烈不建议在内网之外或不可信环境下关闭。

---
- 英文原版：Home Assistant Community Add-on: InfluxDB；链接 https://github.com/hassio-addons/repository/blob/main/influxdb/README.md
- 来源仓库：frenck
