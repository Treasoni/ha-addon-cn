<!-- zh-guide -->
# Scrutiny

## 简介
Scrutiny 是面向 smartd S.M.A.R.T 监控的硬盘健康仪表盘与监控方案，将厂商提供的 S.M.A.R.T 指标与真实故障率数据结合，帮助你在一个 Web 界面中集中查看所有本地硬盘的健康状况。它基于 linuxserver.io 的 docker 镜像构建，支持 Ingress、自动挂载本地磁盘与定时自动更新。

## 安装
1. 在 Home Assistant → 设置 → 加载项 → 商店，添加本商店仓库：
   - Gitee：https://gitee.com/zhqznc_10603234_123/ha-addon
   - GitHub：https://github.com/Treasoni/ha-addon-cn
2. 搜索 scrutiny 并安装。
3. 安装完成后保存配置，按需设置加载项选项，然后启动加载项并查看日志确认一切正常。

## 配置
除下列选项外，其余配置均可直接在应用 WebUI 内完成。加载项会自动挂载所有本地磁盘（/dev/sd*、/dev/nvme* 等），无需手动配置设备。

| 配置键 | 类型/默认值 | 说明 |
|--------|------|-------------|
| `Updates` | 列表，默认 `Hourly` | 更新频率：`Quarterly`（每15分钟）/ `Hourly` / `Daily` / `Weekly` / `Custom` |
| `Updates_custom_time` | 字符串，空 | 自定义更新间隔，需将 `Updates` 设为 `Custom` 后生效，如 `5m`、`2h`、`1w`、`2mo`（分别表示每 5 分钟、每 2 小时、每周、每 2 个月） |
| `TZ` | 字符串，空 | 时区，例如 `Europe/London` |
| `Mode` | 列表 `Collector+WebUI` / `Collector`，空 | 运行模式：`Collector+WebUI`（默认，收集+界面）或 `Collector`（仅收集，会禁用 WebUI 与 InfluxDB） |
| `COLLECTOR_API_ENDPOINT` | 字符串，默认 `http://localhost:8080` | Collector API 端点 URL；模式为 `Collector` 时必填 |
| `COLLECTOR_HOST_ID` | 字符串，默认 `home_assistant` | Collector 的主机标识 |
| `SMARTCTL_COMMAND_DEVICE_TYPE` | 列表 `auto\|ata\|scsi\|sat\|...`，空 | smartctl 命令使用的设备类型 |
| `SMARTCTL_MEGARAID_DISK_NUM` | 整数，空 | MegaRAID 阵列中的磁盘编号 |
| `expose_collector` | 布尔值，空（默认 false） | 是否把 `collector.yaml` 暴露到 `/share/scrutiny` 目录，便于外部查看/修改 |
| `env_vars` | 数组，默认 `[]` | 传递额外环境变量的列表（名称+值），用于自定义脚本等场景 |

> 提示：仅在遇到问题时才启用"完整访问"（Full access）权限。所有场景下 SMART 读取都应无需完整访问即可正常工作。

## 使用 / 访问入口
- **Web 界面**：安装启动后，可从 Home Assistant 侧边栏通过 Ingress 直接打开；也可在浏览器访问 `http://homeassistant:8080`。
- **端口**：`8080`（Web UI）、`8086`（InfluxDB 管理）。默认不对外暴露端口，如需局域网访问请在加载项选项中自行开启。
- **首次访问**：启动后打开 WebUI，在界面内完成配置即可开始查看硬盘健康状态。
- **与 Home Assistant 集成**：通过 `rest` 平台在 `configuration.yaml` 中对接 API。即使不开放端口，API 也在 HA 内部网络可用，可用加载项内部域名查询（例如 `http://db21ed7f-scrutiny:8080`，实际域名以加载项内部域名为准）；如需从局域网访问，请在选项中开放端口并将域名替换为 Home Assistant 的 IP。
  - 摘要数据：`http://<内部域名>:8080/api/summary`
  - 详细数据：`http://<内部域名>:8080/api/device/WWN/details`（WWN 可在 Scrutiny 应用内查看每块硬盘对应值）

## 常见问题
1. **是否需要开启"完整访问"权限？** 不需要。默认情况下 SMART 读取即可正常工作，仅在遇到权限相关问题时才建议启用完整访问。
2. **如何自定义硬盘检测频率？** 将 `Updates` 设为 `Custom`，然后在 `Updates_custom_time` 中填写自然语言间隔，例如 `5m`（每 5 分钟）、`2h`（每 2 小时）、`1w`（每周）、`2mo`（每 2 个月）。
3. **如何在 Home Assistant 中读取硬盘数据？** 使用 `rest` 平台对接 `/api/summary` 或 `/api/device/WWN/details` 接口，即可创建温度、通电时长、SMART 状态等传感器。

---
- 英文原版：Home assistant add-on: Scrutiny（https://github.com/alexbelgium/hassio-addons/blob/master/scrutiny/README.md）
- 来源仓库：alexbelgium
