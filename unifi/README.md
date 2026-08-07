<!-- zh-guide -->
# UniFi Network Application

## 简介
UniFi Network Application 运行 Ubiquiti 官方的 UniFi 网络管理软件，让你通过浏览器管理整个 UniFi 网络。它提供了面向 Home Assistant 的一键安装与运行方案，支持包括树莓派在内的 Home Assistant 常见架构，便于快速部署并保持更新。

> 注意：独立的 UniFi Network Application 已接近生命周期终点（EOL）。Ubiquiti 正转向基于 podman/systemd 的 UniFi OS Server，该方案无法以 Docker/Home Assistant 插件形式运行，也没有从此插件升级到 UniFi OS Server 的路径。只要 Ubiquiti 继续发布独立应用，本插件就能继续使用，但长期使用者建议迁移到专用主机或虚拟机。

## 安装
1. 在 Home Assistant → 设置 → 加载项 → 商店，添加本商店仓库：
   - Gitee：https://gitee.com/zhqznc_10603234_123/homeassistant
   - GitHub：https://github.com/Treasoni/ha-addon-cn
2. 搜索 unifi 并安装。
3. 查看 “UniFi Network Application” 的日志，确认安装运行正常。
4. 点击“打开 Web 界面”（OPEN WEB UI），跟随初始化向导完成设置，并使用刚创建的账号登录。
5. 在左侧选择 UniFi 设备，进入设备更新与设置；在设备设置中的 Inform Host Override 填入运行 Home Assistant 设备的 IP 或主机名，勾选该项并点击 Apply Changes 应用。

## 配置
修改配置后需要重启加载项才会生效。以下是全部可用配置项：

| 配置键 | 类型/默认值 | 说明 |
| --- | --- | --- |
| `log_level` | 可选字符串；默认 `info` | 日志详细程度，可选 `trace`/`debug`/`info`/`notice`/`warning`/`error`/`fatal`。较高级别会自动包含更严重级别的日志；默认 `info` 是推荐值，排查问题时再调高详细程度。 |
| `memory_max` | 可选整数（MB）；默认 `256` | UniFi Network Application 允许占用的最大内存。可调大以降低 CPU 负载，或调小以节省内存。 |
| `memory_init` | 可选整数（MB）；默认 `128` | 启动时初始预留/占用的内存大小。 |

## 使用 / 访问入口
本插件不支持 Ingress，需通过 Web 界面访问：
- 访问地址：`https://[HOST]:8443`（控制器 Web 界面与 API 端口，来自 config.yaml 的 webui/端口定义）。

常用端口（见 config.yaml）：

| 端口 | 用途 |
| --- | --- |
| 8443/tcp | 控制器 Web 界面与 API（主要入口） |
| 8080/tcp | 设备与控制器通信 |
| 8843/tcp | HTTPS 门户重定向 |
| 8880/tcp | HTTP 门户重定向 |
| 3478/udp | STUN |
| 5514/udp | 远程 syslog 调试 |
| 6789/tcp | UniFi 手机 App 测速 |
| 10001/udp | 设备发现 |
| 161/udp | SNMP 访问（默认关闭） |
| 1900/udp | L2 发现端口（默认关闭） |

- 自动备份：UniFi 自带的自动备份功能会把备份写入 `/backup/unifi`，可通过 Home Assistant 的 Samba、Terminal、SSH 等方式访问该目录。
- 手动接纳设备：SSH 登录设备（用户名/密码均为 `ubnt`），执行 `mca-cli`，再运行 `set-inform http://<Home Assistant 的 IP>:8080/inform`（示例：`set-inform http://192.168.1.14:8080/inform`）。

## 常见问题
- **AP 一直处于 “adopting”（接纳中）状态**：请按安装步骤正确配置控制器（重点是 Inform Host Override）。也可使用 Ubiquiti Discovery 工具，或 SSH 到 AP 手动设置 INFORM（见上文“手动接纳设备”）。
- **日志出现 `I/O exception (java.net.ConnectException) caught ... Connection refused`**：这是已知的无害报错，可安全忽略，插件功能正常。
- **无法在 Home Assistant 前端用 panel_iframe 嵌入 UniFi 界面**：这是 UniFi 软件自身安全策略导致的限制。

---
- 英文原版：Home Assistant Community App: UniFi Network Application；链接 https://github.com/hassio-addons/repository/blob/master/unifi/README.md
- 来源仓库：frenck
