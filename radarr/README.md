<!-- zh-guide -->
# Radarr

## 简介

Radarr 是面向 Usenet 和 BitTorrent 用户的电影库管理工具（可视为 Sonarr 的电影版本，类似 Couchpotato）。它可以监控多个 RSS 订阅源来发现新电影，并配合下载客户端与索引器完成抓取、整理和重命名，还可在出现更高质量片源时自动升级库中现有文件的画质。本加载项基于 linuxserver/docker-radarr 镜像构建。

## 安装

1. 在 Home Assistant → 设置 → 加载项 → 商店，添加本商店仓库：
   - Gitee：https://gitee.com/zhqznc_10603234_123/homeassistant
   - GitHub：https://github.com/Treasoni/ha-addon-cn
2. 搜索 radarr 并安装。
3. 启动加载项前，先按需设置下方配置项。
4. 启动加载项，并在日志中确认运行正常。
5. 打开 Web 界面完成 Radarr 自身的设置（索引器、下载客户端、媒体路径等）。

## 配置

| 配置键 | 类型/默认值 | 说明 |
|--------|-------------|------|
| `env_vars` | 列表 / `[]` | 以 `name`/`value` 形式向容器传入额外的环境变量，用于覆盖默认行为 |
| `PGID` | 整数 / `0` | 文件权限组 ID |
| `PUID` | 整数 / `0` | 文件权限用户 ID |
| `TZ` | 字符串 / 空 | 时区，例如 `Europe/London` |
| `connection_mode` | 枚举 / `ingress_noauth` | 连接模式：`ingress_noauth` / `noingress_auth` / `ingress_auth` |
| `localdisks` | 字符串 / 空 | 要挂载的本地磁盘，例如 `sda1,sdb1`，也可使用磁盘标签 |
| `networkdisks` | 字符串 / 空 | 要挂载的 SMB 共享，例如 `//SERVER/SHARE`，多个用逗号分隔 |
| `cifsusername` | 字符串 / 空 | SMB 共享用户名 |
| `cifspassword` | 字符串 / 空 | SMB 共享密码 |
| `cifsdomain` | 字符串 / 空 | SMB 共享所属域 |

### 连接模式说明

- `ingress_noauth`（默认）：启用 Ingress 并关闭本地认证，以便无缝集成到 Home Assistant 侧边栏；请勿将端口直接暴露到外网，以免存在安全风险。
- `noingress_auth`：关闭 Ingress（无法从 Home Assistant 内访问），改为通过外部 URL 访问并启用认证。
- `ingress_auth`：同时启用 Ingress 和认证。

### 示例配置

```yaml
PGID: 0
PUID: 0
TZ: "Asia/Shanghai"
connection_mode: "ingress_noauth"
localdisks: "sda1,sdb1"
networkdisks: "//192.168.1.100/downloads,//nas.local/movies"
cifsusername: "mediauser"
cifspassword: "password123"
cifsdomain: "workgroup"
```

## 使用 / 访问入口

- **Ingress 入口**：加载项启用了 Ingress（入口路径为 `radarr`），可在 Home Assistant 左侧边栏直接点击打开。
- **端口访问**：容器监听 `7878/tcp`（Web 界面），可直接访问 `http://homeassistant:7878`。
- **首次使用**：启动后打开 Web 界面，完成 Radarr 初始化，添加索引器、下载客户端并设置电影媒体库路径。
- **挂载存储**：如需使用外部磁盘或 NAS 共享作为电影库/下载目录，可在配置中通过 `localdisks`、`networkdisks` 及对应 SMB 凭据挂载。

## 常见问题

1. **侧边栏打不开或要求登录？** 检查 `connection_mode`：使用 Ingress 时应保持默认的 `ingress_noauth`（关闭认证），若改为 `ingress_auth` 或 `noingress_auth` 则需要认证，且 `noingress_auth` 会关闭 Ingress 入口。
2. **如何挂载我的电影/下载目录？** 本地磁盘填 `localdisks`（如 `sda1` 或磁盘标签），远程 NAS 填 `networkdisks` 并配合 `cifsusername`/`cifspassword`/`cifsdomain`。
3. **需要给容器传额外参数？** 在 `env_vars` 中按 `name`/`value` 列表添加任意环境变量即可。
4. **配置文件在哪里？** 版本更新后配置迁移到了 `/addon_configs/xxx-radarr_nas`（原名 `/config/addons_config/radarr`），请在迁移后更新你引用旧路径的链接。

---
- 英文原版：Home assistant add-on: Radarr；链接 https://github.com/alexbelgium/hassio-addons/blob/master/radarr/README.md
- 来源仓库：alexbelgium
