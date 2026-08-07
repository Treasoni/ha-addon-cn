<!-- zh-guide -->
# Birdnet-go (customized and built from source)

## 简介

Birdnet-go (dev) 是标准 birdnet-go 加载项的特殊变体。与拉取预编译镜像不同，它会在构建时从 [alexbelgium/birdnet-go](https://github.com/alexbelgium/birdnet-go) 分支编译 BirdNET-Go：构建时先同步该分支与 tphakala/birdnet-go 上游的 main，再合并所有处于评审中的非草稿 Pull Request，因此生成的程序包含上游 main 之外所有当前在审的改动，并启用了 OpenVINO 以利用 Intel CPU/iGPU 加速（仅 amd64 架构）。**⚠️ 这是一个测试构建**，除上述差异外，其余功能与标准 birdnet-go 加载项完全一致。

## 安装

1. 在 Home Assistant → 设置 → 加载项 → 商店，添加本商店仓库：
   - Gitee：https://gitee.com/zhqznc_10603234_123/ha-addon
   - GitHub：https://github.com/Treasoni/ha-addon-cn
2. 搜索 birdnet-go-dev 并安装。
3. 按偏好设置加载项选项，保存并启动，然后打开 Web 界面调整软件设置。

> 提示：需要麦克风——可以使用连接到 Home Assistant 的麦克风，或 RTSP 摄像头的声音流作为音频输入。

## 配置

| 配置键 | 类型 / 默认值 | 说明 |
| ------ | ----------- | ---- |
| `BIRDSONGS_FOLDER` | 字符串，默认 `/config/clips` | 音频剪辑（clips）文件的存储位置；可指向挂载的外部或 SMB 磁盘路径，例如 `/mnt/NAS/Birdnet/` |
| `LOG_MAX_SIZE_MB` | 整数，默认 `50` | 日志文件在轮转前的最大大小（MB） |
| `LOG_MAX_AGE_DAYS` | 整数，默认 `7` | 日志的最大保留天数 |
| `homeassistant_microphone` | 布尔，默认关闭 | 设为 true 时强制音频源为「default」（即 Home Assistant 麦克风） |
| `mqtt_auto_config` | 布尔，默认关闭 | 设为 true 时，自动把 Home Assistant MQTT 加载项（Mosquitto）的凭据写入 BirdNET-Go 的 `config.yaml`，并启用其原生的 Home Assistant MQTT 自动发现 |
| `mariadb_auto_config` | 布尔，默认关闭 | 设为 true 时，自动把 Home Assistant MariaDB 加载项的凭据写入 `output.mysql.*`，并禁用 SQLite |
| `TZ` | 可选字符串，默认空 | 使用的时区，参见 tz database 时区列表 |
| `localdisks` | 可选字符串，默认空 | 要挂载的本地磁盘硬件名或标签，多个以逗号分隔 |
| `networkdisks` | 可选字符串，默认空 | 要挂载的 SMB 共享，多个以逗号分隔，如 `//SERVER/SHARE` |
| `cifsusername` | 可选字符串，默认空 | SMB 共享用户名 |
| `cifspassword` | 可选字符串，默认空 | SMB 共享密码 |
| `cifsdomain` | 可选字符串，默认空 | SMB 共享的域名 |
| `env_vars` | 列表，默认空 | 附加环境变量，通过此选项传入额外环境变量（变量名大小写均可） |

> 说明：更多变量可通过文件浏览类加载项在 `/config/db21ed7f_birdnet-go/config.yaml` 中配置；`mqtt_auto_config` 与 `mariadb_auto_config` 均为选填的自动接线功能。

## 使用 / 访问入口

- **侧边栏**：加载项支持 Ingress，启动后可在 Home Assistant 侧边栏看到 Birdnet-go 图标，点击进入（Ingress 入口为 `ui/dashboard`）。
- **直接访问**：http://homeassistant:8080（容器端口 `8080/tcp` 映射到宿主端口 8080）。
- **遥测端点**：容器端口 `9090/tcp` 映射到宿主端口 9090，用于遥测数据。

## 常见问题

- **这个版本和标准版有什么区别？** 这是测试构建，从 alexbelgium/birdnet-go 分支编译并合并了所有在审的 Pull Request，还启用了 OpenVINO 的 Intel CPU/iGPU 加速；仅支持 amd64 架构，功能与标准版一致但稳定性不作保证。
- **如何接入 RTSP 摄像头音频？** 若使用 VLC 转发音频为 RTSP 流，由于流为 UDP，需要在 `config.yaml` 中把传输配置改为 `udp`，或使用命令行参数 `--rtsptransport udp --rtsp <RTSP地址>`。
- **MQTT 自动配置有什么作用？** 启用 `mqtt_auto_config` 后，加载项会在每次启动时把 HA Mosquitto 的凭据写入 BirdNET-Go 的 `config.yaml`（`realtime.mqtt.*`），并启用原生 Home Assistant MQTT 自动发现；消息默认保留（`retain`）以便重启后状态不丢失。
- **需要什么音频输入？** 需要麦克风——可使用连接到 Home Assistant 的麦克风（配合 `homeassistant_microphone`），或 RTSP 摄像头的声音流。

---
- 英文原版：Home assistant add-on: Birdnet-Go (from source)；链接 https://github.com/alexbelgium/hassio-addons/blob/master/birdnet-go-dev/README.md
- 来源仓库：alexbelgium
