<!-- zh-guide -->
# BirdNET-PiPy

## 简介

BirdNET-PiPy 是一个自托管的鸟类识别系统，使用 BirdNET 深度学习模型从鸟鸣声中识别鸟类，并提供现代化的 Web 仪表盘用于监控识别结果。本 add-on 将上游项目打包进 Home Assistant，支持 Ingress 侧边栏访问；在同一个容器内运行 BirdNET-PiPy 后端服务、Icecast 音频流和 Vue.js 前端。

## 安装

1. 在 Home Assistant → 设置 → 加载项 → 商店，添加本商店仓库：
   - Gitee：https://gitee.com/zhqznc_10603234_123/ha-addon
   - GitHub：https://github.com/Treasoni/ha-addon-cn
2. 搜索 `birdnet-pipy` 并安装。
3. 安装完成后启动 add-on，并查看日志确认运行正常。

## 配置

| 配置键 | 类型 / 默认值 | 说明 |
| --- | --- | --- |
| `env_vars` | 列表 / 空 | 传入容器的额外环境变量（`name`/`value` 形式） |
| `ICECAST_PASSWORD` | 字符串（可选） / 空 | Icecast 音频流的持久密码 |
| `data_location` | 字符串 / 默认 `/config/data` | 持久化数据位置（位于 /config、/share 或 /data 下） |
| `ssl` | 布尔（可选） / 空 | 是否启用 SSL |
| `certfile` | 字符串（可选） / 空 | SSL 证书文件名 |
| `keyfile` | 字符串（可选） / 空 | SSL 私钥文件名 |
| `localdisks` | 字符串（可选） / 空 | 需要挂载的本地磁盘，如 `sda1,sdb1,MYNAS` |
| `networkdisks` | 字符串（可选） / 空 | 需要挂载的 SMB 共享，如 `//SERVER/SHARE` |
| `cifsusername` | 字符串（可选） / 空 | SMB 用户名 |
| `cifspassword` | 字符串（可选） / 空 | SMB 密码 |
| `cifsdomain` | 字符串（可选） / 空 | SMB 域 |

## 使用 / 访问入口

启动后可在 Home Assistant 侧边栏看到 BirdNET-PiPy 图标，点击进入。容器启动后，在 BirdNET-PiPy 界面中配置位置、音频源及其他设置；也可通过端口 8011 直接访问 Web 界面。

## 常见问题

- 音频输入默认使用 Home Assistant 的 PulseAudio 服务。
- 本 add-on 支持挂载本地磁盘与远程 SMB 共享（分别对应 `localdisks` 与 `networkdisks`/`cifs*` 选项）。
- 可通过 addon_config 映射使用自定义脚本，并通过 `env_vars` 选项传入额外环境变量（例如 `STREAM_BITRATE=320k` 控制 Icecast MP3 码率）。
- 除 Ingress 外，也可直接访问所配置的端口。

---
- 英文原版：[Home assistant add-on: BirdNET-PiPy](https://github.com/alexbelgium/hassio-addons/blob/master/birdnet-pipy/README.md)
- 来源仓库：alexbelgium
