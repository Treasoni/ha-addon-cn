<!-- zh-guide -->
# Terminal & SSH

## 简介

Terminal & SSH（终端与 SSH）允许你通过 SSH 远程登录 Home Assistant，或直接在浏览器中使用集成的 Web 终端。借助它，你可以用任意 SSH 客户端访问 Home Assistant 的文件夹，并内置了操作 Home Assistant API 的命令行工具（`ha`）。

## 安装

1. 在 Home Assistant → 设置 → 加载项 → 商店，添加本商店仓库：
   - Gitee：https://gitee.com/zhqznc_10603234_123/ha-addon
   - GitHub：https://github.com/Treasoni/ha-addon-cn
2. 搜索 ssh 并安装。

## 配置

| 配置键 | 类型/默认值 | 说明 |
| --- | --- | --- |
| `authorized_keys` | 字符串列表，默认 `[]` | 允许登录的 SSH **公钥**。可添加多条公钥来授权多个密钥；若添加时遇到 YAML 语法问题，请用双引号包裹公钥。 |
| `password` | 密码（字符串），默认 `""` | 设置登录密码。**不推荐**使用此方式；启用密码登录会禁用密钥登录，二者不能同时生效。 |
| `apks` | 字符串列表，默认 `[]` | 容器启动时要额外安装的 Alpine 软件包。 |
| `server.tcp_forwarding` | 布尔值，默认 `false` | 是否允许 SSH 的 TCP 端口转发（`-L` / `-R`）。开启会降低 SSH 服务器的安全性。 |

## 使用 / 访问入口

- **Web 终端（Ingress）**：在加载项详情页点击"打开 Web UI"按钮即可访问；在详情页开启"显示在侧边栏"，会在侧边栏添加快捷方式，方便快速进入。
  - 复制文本：按住 `SHIFT` 键用鼠标拖选文本，松开左键即复制到剪贴板。
  - 粘贴文本：按 `SHIFT + INSERT`。
- **SSH 服务器**：默认**禁用**（端口未映射）。如需用 SSH 客户端（如 PuTTY、Linux 终端）远程登录：
  1. 在"网络"配置的输入框中填写要映射到宿主机的 TCP 端口（SSH 协议标准端口为 `22`）。
  2. 配置认证凭据（密码或公钥）。
  3. 使用用户名 `root` 连接指定端口。
  - 清除端口输入框、保存并重启，即可再次禁用远程 SSH 访问。
- **常用命令**：内置 Home Assistant CLI，试试 `ha help`；配置文件目录位于 `/config`。

## 常见问题

- **更新后 RSA 密钥无法登录？** 使用 SHA-1 算法生成的 RSA 密钥已被 OpenSSH 禁用（安全漏洞）。请改用更安全的算法生成新密钥，或切换为 ECDSA、Ed25519 类型密钥——生成密钥时直接选择 **ECDSA** 类型即可。
- **能否安装软件包或以 root 身份操作？** 不能。受 Home Assistant 限制，此加载项无法以 root 安装软件包。需要在容器内安装额外软件包时，请使用 `apks` 配置项在启动时自动安装。
- **SSH 服务器开启后安全吗？** 开启 SSH 服务器可能让互联网上的人尝试访问你的系统，安全性还取决于你的网络、路由器与防火墙设置。若不了解影响，建议保持 SSH 服务器关闭，仅使用 Web 终端。

---
- 英文原版：Home Assistant App: SSH server；链接 https://github.com/home-assistant/addons/blob/master/ssh/README.md
- 来源仓库：official
