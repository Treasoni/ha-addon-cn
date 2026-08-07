<!-- zh-guide -->
# Matter Server

## 简介
本加载项为 Home Assistant Core 提供 Matter WebSocket 服务器。Matter（原 Connected Home over IP / CHIP）是基于 IPv6 的智能家居标准；本加载项作为 Matter 控制器，允许你配网（commission）并控制 Matter 设备，Home Assistant 的 Matter 集成通过 WebSocket 与本服务器通信。

## 安装
1. 在 Home Assistant → 设置 → 加载项 → 商店，添加本商店仓库：
   - Gitee：https://gitee.com/zhqznc_10603234_123/ha-addon
   - GitHub：https://github.com/Treasoni/ha-addon-cn
2. 搜索 matter_server 并安装。

## 配置
| 配置键 | 类型 / 默认值 | 说明 |
| --- | --- | --- |
| `log_level` | 枚举（`debug`/`info`/`notice`/`warn`/`error`/`fatal`/`verbose`/`warning`/`critical`）/ 默认 `info` | Matter 服务器的日志级别 |
| `beta` | 布尔 / `false` | 是否使用 beta 版本服务器 |
| `enable_test_net_dcl` | 布尔 / `false` | 是否启用测试网络 DCL，用于配网使用测试/开发证书的未认证 DIY 设备 |
| `time_sync` | 枚举（`auto`/`on`/`off`）/ 默认 `auto` | 是否向 Matter 设备同步时间：`auto` 仅在主机时钟已 NTP 校准时启用，`on` 始终启用（NTP 未校准时给出警告），`off` 关闭 |
| `default_fabric_label` | 字符串（1–32 字符）/ 空 | 固定 fabric 标签；设置后将阻止通过 WebSocket API 修改标签 |
| `ble_proxy` | 布尔 / 空 | 是否启用 BLE（蓝牙）代理 |
| `bluetooth_adapter_id` | 整数 / 空 | 使用的蓝牙适配器 ID |
| `matter_server_args` | 字符串列表 / 空 | 传给 Matter 服务器的额外命令行参数 |
| `matter_server_env_vars` | 字符串列表 / 空 | 传给 Matter 服务器的额外环境变量（`KEY=VALUE` 格式） |
| `matter_server_version` | 字符串 / 空 | 指定安装的 Matter 服务器版本 |

## 使用 / 访问入口
启动后可在 Home Assistant 侧边栏看到 Matter Server 图标，点击进入 Web 面板（可查看设备与 Thread/Wi-Fi 网络拓扑）。配网与设备控制请在 Home Assistant 的「设置 → 设备与服务 → Matter」集成中完成。

## 常见问题
- **从 8.x 升级**：升级到 9.x 前请先阅读 9.0.0 的版本说明；首次启动会自动迁移现有数据，需要较长时间，请在日志中等待迁移完成后再操作。
- **升级前备份**：升级前建议勾选「创建备份」；如果启用了看门狗（watchdog）且 Matter 节点较多，建议在初次迁移时暂时关闭看门狗，避免迁移中途被重启。
- **测试网络 DCL**：旧版本默认允许配网使用测试/开发证书的未认证设备；新版本需先开启 `enable_test_net_dcl` 才能配网这类设备。
- **资源占用**：基于 matter.js 的新版服务器内存占用约为旧版的两倍，请确保宿主有足够的空闲内存。
- **无法回退**：迁移到基于 matter.js 的 Matter Server（9.x）后，无法回退到旧版 Python 版服务器。

---
- 英文原版：Home Assistant App: Matter Server（[链接](https://github.com/home-assistant/addons/blob/master/matter_server/README.md)）
- 来源仓库：official
