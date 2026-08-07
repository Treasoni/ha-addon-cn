<!-- zh-guide -->
# Z-Wave JS

## 简介

通过 USB Z-Wave 控制器，让 Home Assistant 与 Z-Wave 网络通信，管理和控制 Z-Wave 设备。本加载项集成了 Z-Wave JS 驱动与 Z-Wave JS UI 管理界面，是 Home Assistant 官方推荐的 Z-Wave 解决方案。

## 安装

1. 在 Home Assistant → 设置 → 加载项 → 商店，添加本商店仓库：
   - Gitee：https://gitee.com/zhqznc_10603234_123/ha-addon
   - GitHub：https://github.com/Treasoni/ha-addon-cn
2. 搜索 zwave_js 并安装。
3. 安装后需要配置 Z-Wave 控制器串口，并添加 Home Assistant 的 Z-Wave JS 集成（参见下方"使用/访问入口"）。

## 配置

配置键 | 类型/默认值 | 说明
--- | --- | ---
`device` | 字符串（可选） | Z-Wave 控制器串口设备路径，例如 `/dev/ttyUSB0`、`/dev/ttyAMA0`、`/dev/ttyACM0`，推荐使用 `by-id` 路径（如 `/dev/serial/by-id/usb-0658_0200-if00`），避免设备变更时路径失效。`device` 与 `socket` 至少配置其一
`socket` | 字符串（可选） | 以 socket 方式连接 Z-Wave 控制器，作为 `device` 的替代连接方式
`log_level` | 列表，默认 `info` | Z-Wave JS 日志级别：`silly`、`debug`、`verbose`、`http`、`info`、`warn`、`error`；未设置时沿用 Supervisor 的日志级别
`log_to_file` | 布尔，默认 `false` | 开启后将日志写入 `/addon_configs/core_zwave_js` 目录（`.log` 后缀文件）
`log_max_files` | 整数，默认 `7` | `log_to_file` 开启时，按天保留的最大日志文件数
`rf_region` | 列表，默认 `Automatic` | 射频区域：`Automatic`、Australia/New Zealand、China、Europe、Europe (Long Range)、Hong Kong、India、Israel、Japan、Korea、Russia、USA、USA (Long Range)。`Automatic` 根据 Home Assistant 中设置的国家自动选择
`soft_reset` | 列表，默认 `Automatic` | 500 系列控制器的软复位处理方式：`Automatic`（自动判断）、`Enabled`（强制启用）、`Disabled`（强制禁用）；在虚拟机环境中自动禁用软复位
`s0_legacy_key` | 32 位十六进制（可选） | S0 安全网络密钥，用于加入 S0 安全设备；留空时启动自动生成
`s2_access_control_key` | 32 位十六进制（可选） | S2 门锁、车库门等设备所需的安全密钥；留空时启动自动生成
`s2_authenticated_key` | 32 位十六进制（可选） | S2 安防系统、传感器、照明等设备所需的安全密钥；留空时启动自动生成
`s2_unauthenticated_key` | 32 位十六进制（可选） | S2 无身份验证设备的安全密钥；留空时启动自动生成
`lr_s2_access_control_key` | 32 位十六进制（可选） | Z-Wave Long Range 设备所需的安全密钥；留空时启动自动生成
`lr_s2_authenticated_key` | 32 位十六进制（可选） | Z-Wave Long Range 设备所需的安全密钥；留空时启动自动生成
`network_key` | 32 位十六进制（已废弃） | 旧版单一网络密钥选项；首次启动会自动迁移到 `s0_legacy_key`。如与 `s0_legacy_key` 同时设置且值不一致将无法启动
`disable_controller_recovery` | 布尔（可选） | 关闭控制器无响应时的自动恢复流程；高级选项，仅排障时使用
`disable_watchdog` | 布尔（可选） | 禁止启用控制器硬件看门狗；高级选项，仅排障时使用
`safe_mode` | 布尔（可选） | 启用安全模式，网络性能显著下降，但有助于排查启动故障、抓取日志；高级选项，应少用

## 使用 / 访问入口

- **管理界面（Ingress）**：安装并启动后，通过 Home Assistant 侧边栏的 **Z-Wave** 面板进入 Z-Wave JS UI 管理界面（ingress 端口 8091），可查看节点、执行配对/移除、查看网络图、管理配置参数、进行固件升级等。
- **集成接入**：加载项启动后会自动向 Home Assistant 广播 `zwave_js` 发现信息，按提示在 设置 → 设备与服务 中完成 Z-Wave JS 集成添加（Z-Wave JS 服务监听端口 3000）。集成使用说明见官方文档：<https://www.home-assistant.io/integrations/zwave_js>。
- **查找串口设备**：在 设置 → 系统 → 硬件 → 右上角"⋯" → "所有硬件" 中查看控制器设备路径，优先使用 `by-id` 路径。

## 常见问题

1. **找不到或选不对串口设备**：在 设置 → 系统 → 硬件 → "所有硬件" 中查找 USB 设备路径；若系统新增了其他设备导致路径变化，`by-id` 路径可避免此问题。
2. **安全密钥丢失怎么办**：若密钥留空，加载项会自动生成。请务必备份这六个密钥——丢失后无法再与已加密配对（如门锁）的设备通信，可能需要重置控制器和设备。不要使用文档中的示例密钥，加载项检测到示例密钥会拒绝启动。
3. **网络故障排查**：将 `log_level` 调为 `debug` 并开启 `log_to_file` 抓取日志；Z-Wave JS 的网络缓存位于 `/addon_configs/core_zwave_js/cache`，可提供给开发者协助分析。若加载项无法启动，可临时开启 `safe_mode`。

---
- 英文原版：[Home Assistant App: Z-Wave JS](https://github.com/home-assistant/addons/blob/master/zwave_js/README.md)
- 来源仓库：official
