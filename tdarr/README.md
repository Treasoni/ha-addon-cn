<!-- zh-guide -->
# Tdarr

## 简介

Tdarr 是一个分布式转码自动化系统，使用 FFmpeg/HandBrake 自动化媒体库的转码与封装管理，确保文件的编码格式、音视频流和容器都符合你的要求。它支持分布式处理，可以把你闲置的设备作为 Tdarr Node 加入（支持 Windows、Linux 含 ARM、macOS），并提供基于插件的流程系统与硬件加速支持。本加载项基于 hurlenko/Tdarr 镜像构建。

## 安装

1. 在 Home Assistant → 设置 → 加载项 → 商店，添加本商店仓库：
   - Gitee：https://gitee.com/zhqznc_10603234_123/ha-addon
   - GitHub：https://github.com/Treasoni/ha-addon-cn
2. 搜索 `tdarr` 并安装。

## 配置

| 配置键 | 类型 / 默认值 | 说明 |
|--------|--------------|------|
| `CONFIG_LOCATION` | 字符串 / 默认 `/config/addons_config/tdarr` | Tdarr 配置存放路径 |
| `env_vars` | 列表 / 空 | 额外环境变量列表（每项含 `name` 和 `value`） |
| `TZ` | 字符串 / 空 | 时区（如 `Europe/London`） |
| `localdisks` | 字符串 / 空 | 要挂载的本地磁盘（如 `sda1,sdb1,MYNAS`） |
| `networkdisks` | 字符串 / 空 | 要挂载的 SMB 共享（如 `//SERVER/SHARE`） |
| `cifsusername` | 字符串 / 空 | SMB 共享用户名 |
| `cifspassword` | 字符串 / 空 | SMB 共享密码 |
| `cifsdomain` | 字符串 / 空 | SMB 共享域名 |

## 使用 / 访问入口

Web 界面位于宿主端口 8265，Tdarr 服务器端口为 8266（用于外部 Tdarr Node 连接）。

## 常见问题

- **分布式转码**：在 Web 界面中配置好媒体库与转码设置后，可在其他机器安装 Tdarr Node 并指向 Home Assistant 的 8266 端口，节点会自动注册并出现在 Web 界面中。
- **硬件加速**：加载项已映射 `/dev/dri` 等设备并设置相关环境变量，支持 Intel QuickSync、NVIDIA NVENC、AMD VCE。可在 Tdarr Web 界面的 FFmpeg/HandBrake 设置中配置硬件加速。
- **配置与挂载**：配置存放在 `CONFIG_LOCATION` 指定的目录；支持挂载本地磁盘与远程 SMB 共享，通过 `localdisks`/`networkdisks` 及 `cifs*` 选项配置。

---
- 英文原版：[Tdarr](https://github.com/alexbelgium/hassio-addons/blob/master/tdarr/README.md)
- 来源仓库：alexbelgium
