<!-- zh-guide -->
# Prowlarr NAS

## 简介

Prowlarr 是一款基于流行的 arr .NET/React 技术栈构建的索引器（Indexer）管理与代理工具，用于统一管理 Torrent 与 Usenet 索引器，并与 Sonarr、Radarr、Lidarr、Readarr 等 PVR 应用无缝集成。它内置了各应用的索引器同步，无需在每个应用中重复配置。本加载项基于 linuxserver/docker-prowlarr 镜像构建。

## 安装

1. 在 Home Assistant → 设置 → 加载项 → 商店，添加本商店仓库：
   - Gitee：https://gitee.com/zhqznc_10603234_123/ha-addon
   - GitHub：https://github.com/Treasoni/ha-addon-cn
2. 搜索 prowlarr 并安装。
3. 安装后保存配置、启动加载项，并检查日志确认一切正常。

## 配置

以下选项可在加载项配置中设置；除这些选项外，其余配置均可直接在 Prowlarr 的 WebUI 中完成。

| 配置键 | 类型 / 默认值 | 说明 |
|--------|--------------|------|
| `env_vars` | list（名称/值对） | 追加自定义环境变量（变量名大写或小写均可） |
| `PGID` | int / `0` | 文件权限的组 ID |
| `PUID` | int / `0` | 文件权限的用户 ID |
| `TZ` | str / 空 | 时区（如 `Europe/London`） |
| `connection_mode` | list / `ingress_noauth` | 连接模式，可选 `ingress_noauth` / `noingress_auth` / `ingress_auth` |
| `localdisks` | str / 空 | 挂载的本地磁盘（如 `sda1,sdb1,MYNAS`） |
| `networkdisks` | str / 空 | 挂载的 SMB 共享（如 `//SERVER/SHARE`） |
| `cifsusername` | str / 空 | SMB 共享的用户名 |
| `cifspassword` | str / 空 | SMB 共享的密码 |
| `cifsdomain` | str / 空 | SMB 共享的域 |
| `smbv1` | bool / `false` | 是否启用 SMB v1 协议 |

### 连接模式说明

- `ingress_noauth`（默认）：关闭认证，便于无缝接入 Home Assistant 侧边栏的 Ingress 访问。
- `noingress_auth`：关闭 Ingress，改为通过外部 URL 访问并启用登录认证。
- `ingress_auth`：同时启用 Ingress 与登录认证。

## 使用 / 访问入口

- 默认通过 Home Assistant 侧边栏的 Ingress 入口访问 WebUI。
- 也可通过 `http://homeassistant:9696` 直接访问 Web 界面（端口 9696/tcp）。
- 首次访问后在 WebUI 中配置你使用的索引器，即可通过 Prowlarr 统一管理并为 Sonarr、Radarr、Lidarr、Readarr 提供索引器。
- 本加载项支持挂载本地磁盘与远程 SMB 共享，便于在媒体库中检索文件。

## 常见问题

1. **连接模式该如何选择？** 默认 `ingress_noauth` 适合只在 Home Assistant 侧边栏使用；如需通过外部 URL 访问并加上登录认证，可改用 `noingress_auth` 或 `ingress_auth`。
2. **如何挂载网络共享？** 通过 `networkdisks` 填写 SMB 共享地址（如 `//192.168.1.100/indexers`），并配合 `cifsusername`、`cifspassword`、`cifsdomain` 配置凭据；老旧的 SMB v1 协议需将 `smbv1` 设为 `true`。
3. **Web 界面无法访问？** 检查加载项是否已启动、日志是否正常，并确认连接模式与端口（9696）配置无误。

---
- 英文原版：Home assistant add-on: Prowlarr
- 链接：https://github.com/alexbelgium/hassio-addons/blob/master/prowlarr/README.md
- 来源仓库：alexbelgium
