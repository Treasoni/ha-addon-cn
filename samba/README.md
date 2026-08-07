<!-- zh-guide -->
# Samba share

## 简介
Samba share 加载项通过 SMB/CIFS 协议将 Home Assistant 的文件夹共享到本地网络，方便你用 Windows、macOS 等设备通过网络直接访问和编辑配置文件。支持 aarch64 和 amd64 架构。

## 安装
1. 在 Home Assistant → 设置 → 加载项 → 商店，添加本商店仓库：
   - Gitee：https://gitee.com/zhqznc_10603234_123/ha-addon
   - GitHub：https://github.com/Treasoni/ha-addon-cn
2. 搜索 samba 并安装。

## 配置
以下选项来自 `config.yaml`，按需调整：

| 配置键 | 类型/默认值 | 说明 |
| --- | --- | --- |
| `username` | str，默认 `homeassistant` | Samba 认证用户名（必填）。与 Home Assistant 登录凭据无关，可任意指定。 |
| `password` | password，默认空 | 与用户名对应的认证密码（必填）。 |
| `workgroup` | str，默认 `WORKGROUP` | 工作组名称，按你的网络环境修改。 |
| `enabled_shares` | 列表，默认启用全部 | 可访问的共享目录列表；移除或注释掉某项后该共享将不可访问，可随时重新启用。可选值：`local_apps`、`app_configs`、`addons`、`addon_configs`、`backup`、`config`、`media`、`share`、`ssl`。 |
| `compatibility_mode` | bool，默认 `false` | 设为 `true` 启用旧版 Samba 协议（NT1），可解决某些不支持新协议的客户端连不上的问题，但会降低安全性，仅在必要时开启。 |
| `apple_compatibility_mode` | bool，默认 `true` | 启用与 Apple 设备的互操作配置；对于不支持扩展属性（xattr）的文件系统（如 exFAT），可能需要关闭此项。 |
| `netbios` | bool，默认 `true` | NetBIOS 是访问 SMB/CIFS 共享的旧协议。面向 Windows Vista 之前（如 Win95/98/ME/NT/2000/XP）、macOS 10.9（Mavericks）之前的旧客户端需开启；现代安装建议关闭。关闭后仅开放 445 端口（139 被阻断）。 |
| `local_master` | bool，默认 `true` | 在启用 NetBIOS 时，尝试成为所在子网的本地主浏览器。 |
| `network_discovery` | bool，默认 `true` | 通过 WSDD 在网络上广播主机，使其自动出现在 Windows 资源管理器的"网络"中。关闭只影响自动发现，不影响共享访问，可通过主机名或 IP 连接。 |
| `server_signing` | 列表 `default\|auto\|mandatory\|disabled`，默认 `default` | 配置 SMB 服务器签名要求，可提升安全性、防止中间人攻击；具体取值含义见 smb.conf 手册。 |
| `veto_files` | 字符串列表，默认 `._*`、`.DS_Store`、`Thumbs.db`、`icon?`、`.Trashes` | 既不可见也不可访问的文件列表，用于阻止客户端在共享里写入临时隐藏文件（如 macOS 的 `.DS_Store`、Windows 的 `Thumbs.db`）。 |
| `allow_hosts` | 字符串列表，默认内网私有网段 | 允许访问共享的主机/网段列表。 |

## 使用 / 访问入口
本加载项使用 `host_network: true` 直接监听宿主网络，无 Web 界面入口，通过 SMB 共享访问：

- Windows：在资源管理器地址栏输入 `\\<IP 地址>\` 连接。
- macOS：在访达中连接 `smb://<IP 地址>`。

连接时使用上面配置的用户名和密码（非 Home Assistant 登录账号）。默认共享如下：

| 共享名 | 内容 |
| --- | --- |
| `local_apps` | 本地应用（add-ons）目录 |
| `app_configs` | 应用的配置文件 |
| `backup` | Home Assistant 备份 |
| `config` | Home Assistant 配置目录 |
| `media` | 本地媒体文件 |
| `share` | 应用与 Home Assistant 之间共享的数据 |
| `ssl` | SSL 证书 |

注意：`local_apps` 和 `app_configs` 曾分别命名为 `addons` 和 `addon_configs`。旧名称仍会保留并指向相同目录以便迁移过渡，但已标记弃用，建议尽快切换到新名称（连接旧名称共享时会看到提示日志）。

## 常见问题
1. **连不上共享？** 确认已设置用户名和密码，且 `allow_hosts` 包含你设备的网段；旧客户端连不上时可尝试开启 `compatibility_mode`。
2. **密码/用户名和 Home Assistant 登录有关系吗？** 没有。Samba 的用户名密码与 HA 登录凭据完全独立，可任意设置。
3. **关闭 `network_discovery` 或 `netbios` 后还能访问吗？** 可以。这两个选项只影响网络自动发现，按主机名或 IP 地址直接连接不受影响。

---
- 英文原版：Home Assistant App: Samba share；链接 https://github.com/home-assistant/addons/blob/master/samba/README.md
- 来源仓库：official
