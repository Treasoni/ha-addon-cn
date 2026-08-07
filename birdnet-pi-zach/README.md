<!-- zh-guide -->
# BirdNET-Pi (zach7036)

## 简介

BirdNET-Pi (zach7036) 是一款实时声学鸟类分类与监测系统，AI 解决方案最初由 @mcguirepr89 开发（https://github.com/mcguirepr89/BirdNET-Pi）。本加载项构建于 [@zach7036 的 BirdNET-Pi-Enhanced-Version 分支](https://github.com/zach7036/BirdNET-Pi-Enhanced-Version)，该分支增加了新功能并更新了界面。如需基于 @Nachtzuster 分支的加载项，请使用单独的 `birdnet-pi`。加载项具备以下特性：稳定的 LinuxServer 基础镜像、直接使用 Home Assistant 的 PulseAudio 音频服务器、使用 tmpfs 在内存中存放临时文件以减少磁盘磨损、将配置文件暴露到 `/config` 便于持久化与访问、支持修改鸟鸣存储目录（建议放到外部硬盘），并支持 Ingress 以便安全远程访问。

## 安装

1. 在 Home Assistant → 设置 → 加载项 → 商店，添加本商店仓库：
   - Gitee：https://gitee.com/zhqznc_10603234_123/ha-addon
   - GitHub：https://github.com/Treasoni/ha-addon-cn
2. 搜索 birdnet-pi-zach 并安装。
3. 按偏好设置加载项选项，保存并启动；首次启动后打开 Web 界面调整软件设置。

> 提示：需要麦克风——可以使用连接到 Home Assistant 的麦克风，或 RTSP 摄像头的声音流作为音频输入。

## 配置

| 配置键 | 类型 / 默认值 | 说明 |
| ------ | ----------- | ---- |
| `BIRDSONGS_FOLDER` | 字符串，默认 `/config/BirdSongs` | 存储鸟鸣录音文件的目录；建议使用 SSD 或外部硬盘，避免影响分析性能 |
| `LIVESTREAM_BOOT_ENABLED` | 布尔，默认关闭 | 是否在启动时自动开始直播流（否则需在设置中手动开启） |
| `MQTT_DISABLED` | 布尔，默认开启 | 是否禁用自动 MQTT 发布；仅当本地已有可用的 broker 时才应禁用 |
| `Use_tphakala_model_v2` | 布尔，默认关闭 | 切换到 BirdNET-Go 的分类器文件（tphakala 的 v2 模型） |
| `TZ` | 字符串，默认 `Europe/Paris` | 使用的时区，参见 tz database 时区列表 |
| `ssl` | 布尔，默认关闭 | 是否启用 SSL（HTTPS） |
| `certfile` | 字符串，默认 `fullchain.pem` | SSL 证书文件，需存放在 `/ssl/` 目录下 |
| `keyfile` | 字符串，默认 `privkey.pem` | SSL 私钥文件，需存放在 `/ssl/` 目录下 |
| `pi_password` | 密码，默认空 | Web 终端（terminal）用户 `pi` 的访问密码 |
| `MQTT_HOST_manual` | 可选字符串，默认空 | 手动指定 MQTT 服务器主机 |
| `MQTT_USER_manual` | 可选字符串，默认空 | 手动指定 MQTT 用户名 |
| `MQTT_PASSWORD_manual` | 可选密码，默认空 | 手动指定 MQTT 密码 |
| `MQTT_PORT_manual` | 可选整数，默认空 | 手动指定 MQTT 端口 |
| `localdisks` | 可选字符串，默认空 | 要挂载的本地磁盘硬件名或标签，多个以逗号分隔，如 `sda1,sdb1,MYNAS` |
| `networkdisks` | 可选字符串，默认空 | 要挂载的 SMB 共享，多个以逗号分隔，如 `//SERVER/SHARE` |
| `cifsusername` | 可选字符串，默认空 | SMB 共享用户名（对所有共享通用） |
| `cifspassword` | 可选字符串，默认空 | SMB 共享密码 |
| `cifsdomain` | 可选字符串，默认空 | SMB 共享的域名 |
| `env_vars` | 列表，默认空 | 附加环境变量，通过此选项传入额外环境变量（变量名大小写均可） |

> 说明：更多变量可通过文件浏览类加载项在 `/config/db21ed7f_birdnet-pi-zach/config.yaml` 中配置。

## 使用 / 访问入口

- **侧边栏**：加载项支持 Ingress，启动后可在 Home Assistant 侧边栏看到 BirdNET-Pi 图标，点击进入（Ingress 无需密码，但部分功能不可用）。
- **直接访问**：http://homeassistant:8081（容器端口 `8081/tcp` 映射到宿主端口 8081）。提示输入密码时用户名是 `birdnet`，密码为你在 birdnet.conf 中设置的密码（默认为空）。
- **Web 终端**：用户名 `pi`，密码为加载项选项 `pi_password` 中设置的值。
- **可选 SSL**：可安装 Let's Encrypt 加载项生成证书后启用 `ssl` 选项；也可将端口 `80/tcp` 暴露为 80 并把访问地址设为 https，由 caddy 自动生成证书。

## 常见问题

- **这个版本和标准 `birdnet-pi` 有什么区别？** 本加载项基于 @zach7036 的 BirdNET-Pi-Enhanced-Version 分支，增加了新功能并更新了界面；标准版基于 @Nachtzuster 的分支。
- **如何提高检测准确率？** 在「终端」页使用 `alsamixer` 调整声卡增益，保证声音足够大但不过载；不建议使用高通滤波，因为模型分析 0–15kHz 全频段。
- **推荐使用哪种麦克风？** 综合灵敏度与性价比，EM272（配 Ugreen 的 aux 转 usb 转接头）灵敏度最佳，Boya By-LM40 性价比最高；aux 转 usb 适配器建议选 KT0210 芯片（如 Ugreen），ALC 芯片的适配器可能无法识别。
- **MQTT 集成如何工作？** 安装并启用 MQTT 后，加载项会自动在 birdnet 主题下发布每次检测到的物种；也可用 Apprise 通过 MQTT 发送通知。

---
- 英文原版：Home assistant add-on: BirdNET-Pi (zach7036)；链接 https://github.com/alexbelgium/hassio-addons/blob/master/birdnet-pi-zach/README.md
- 来源仓库：alexbelgium
