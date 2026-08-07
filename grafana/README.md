<!-- zh-guide -->
# Grafana

## 简介

Grafana 是开放、漂亮的分析与监控平台，可用于查询、可视化、告警和理解你的各项指标，无论这些指标存储在哪里。你可以创建、探索并分享仪表盘，借助直观的图表来了解你的智能家居系统。将本加载项与 InfluxDB 加载项搭配使用，可以获得对家庭环境的强大洞察。

## 安装

1. 在 Home Assistant → 设置 → 加载项 → 商店，添加本商店仓库：
   - Gitee：https://gitee.com/zhqznc_10603234_123/ha-addon
   - GitHub：https://github.com/Treasoni/ha-addon-cn
2. 搜索 grafana 并安装。

## 配置

在加载项“配置”页修改配置后，需要重启加载项才能生效。可选配置键如下：

| 配置键 | 类型/默认值 | 说明 |
| ------ | ----------- | ---- |
| `log_level` | 可选 `list(trace|debug|info|notice|warning|error|fatal)`，默认 `info` | 日志输出详细程度：`trace` 输出全部细节；`debug` 输出调试信息；`info` 常规事件；`warning` 非错误的异常事件；`error` 运行时错误；`fatal` 致命错误。更高级别会自动包含更低级别的日志，默认 `info` 是推荐设置 |
| `grafana_ingress_user` | 可选 `str`，默认 `空` | 使用 Ingress 时 Grafana 默认会自动以 `admin` 用户名登录；如需使用其他用户，可在此指定该用户名 |
| `ssl` | `bool`，默认 `true` | 是否在 Grafana Web 界面启用 SSL（HTTPS），设为 `true` 启用 |
| `certfile` | `str`，默认 `fullchain.pem` | 用于 SSL 的证书文件，必须存放在 `/ssl/` 目录 |
| `keyfile` | `str`，默认 `privkey.pem` | 用于 SSL 的私钥文件，必须存放在 `/ssl/` 目录 |
| `plugins` | 列表/字符串列表，默认 `空` | 额外安装到 Grafana 的插件（插件列表见 Grafana 插件官网）；添加插件会延长启动时间 |
| `custom_plugins` | 列表/对象列表（含 `name`、`url`、`unsigned` 子键），默认 `空` | 从指定 URL 安装的自定义 Grafana 插件，必须提供 `url` 属性 |
| `custom_plugins.name` | `str`，默认 `空` | 自定义插件的名称 |
| `custom_plugins.url` | `str`，默认 `空` | 自定义插件的下载地址（URL） |
| `custom_plugins.unsigned` | 可选 `bool`，默认 `空` | 如需安装未签名的插件，须将此项设为 `true` |
| `env_vars` | 列表/对象列表（含 `name`、`value` 子键），默认 `空` | 通过环境变量调整 Grafana 的任意配置。仅接受以 `GF_` 开头的环境变量，用法详见 Grafana 官方文档 |
| `env_vars.name` | `str`，默认 `空` | 要设置的环境变量名 |
| `env_vars.value` | `str`，默认 `空` | 要设置的环境变量值 |

## 使用 / 访问入口

- **Web 界面**：加载项支持 Ingress，启动后可在 Home Assistant 侧边栏看到 Grafana 图标，点击进入。
- **默认账号**：默认登录用户为 `admin`，密码为 `hassio`。受实现所限，该密码无法直接修改，但你可以删除并新建一个用户，并在新建后更新 `grafana_ingress_user` 配置。
- **直接访问（可选）**：端口 `80/tcp` 为直连端口（Ingress 场景下无需使用），仅在需要绕过 Ingress 直接访问时才会用到。

## 常见问题

- **忘记密码怎么办？** 默认密码为 `hassio`。由于实现限制密码无法直接修改，可删除 `admin` 用户并新建用户，同时更新 `grafana_ingress_user` 配置项。
- **如何连接 InfluxDB 加载项？** 在 InfluxDB 中为 Grafana 创建专用用户和数据库，然后在 Grafana 中添加数据源：类型选择 InfluxDB，URL 填 `http://a0d7b954-influxdb:8086`，访问方式选“服务器（默认）”，再填写对应的数据库、用户名和密码。
- **面板图片无法渲染？** 在 ARM 设备（如树莓派）上会出现“To render a panel image, you must install the Grafana Image Renderer plugin”的提示，因为 Grafana Image Renderer 插件不支持这些设备。
- **如何开启匿名访问？** 通过加载项配置暴露端口，并设置 `GF_AUTH_ANONYMOUS_ENABLED`、`GF_AUTH_ANONYMOUS_ORG_NAME`、`GF_AUTH_ANONYMOUS_ORG_ROLE` 等环境变量；注意 Home Assistant Cloud 下无法启用匿名或非管理员访问。

---
- 英文原版：Home Assistant Community Add-on: Grafana；链接 https://github.com/hassio-addons/repository/blob/main/grafana/README.md
- 来源仓库：frenck
