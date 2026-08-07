<!-- zh-guide -->
# Node-RED

## 简介

Node-RED 是一款基于流程（Flow）的编程工具，用于把硬件设备、API 和在线服务以可视化方式「接线」在一起。它提供基于浏览器的编辑器，让你能利用调色板中丰富的节点快速搭建自动化流程，并一键部署到运行时。本加载项已针对 Home Assistant 预配置，开箱即用，无需手动设置服务器连接。

## 安装

1. 在 Home Assistant → 设置 → 加载项 → 商店，添加本商店仓库：
   - Gitee：https://gitee.com/zhqznc_10603234_123/ha-addon
   - GitHub：https://github.com/Treasoni/ha-addon-cn
2. 搜索 node-red 并安装。
3. 启动「Node-RED」加载项，并查看日志确认运行正常。
4. 点击「OPEN WEB UI」按钮即可进入 Node-RED 编辑器。

**说明**：本加载项开箱即已预配置，无需修改服务器连接设置即可使用。

## 配置

配置修改后需要重启加载项才能生效。主要配置项如下：

| 配置键 | 类型/默认值 | 说明 |
| --- | --- | --- |
| `log_level` | 列表（默认 `info`） | 日志输出级别：`trace` / `debug` / `info` / `warning` / `error` / `fatal`，级别越高越详细，排查问题时使用 |
| `credential_secret` | 密码（可选） | Node-RED 用于加密存储凭据的密钥，可自定义；一旦设置请勿更改，否则已有凭据将无法解密。若手动启用了项目功能，此项会被忽略 |
| `theme` | 列表（默认 `default`） | 编辑器主题，可选 `aurora`、`dark`、`dracula`、`monokai`、`night-owl`、`oled`、`solarized-dark`、`tokyo-night` 等数十种 |
| `http_node.username` | 字符串（默认空） | 访问 HTTP 节点（`httpNodeRoot`）的认证用户名 |
| `http_node.password` | 密码（默认空） | 访问 HTTP 节点的认证密码 |
| `http_static.username` | 字符串（默认空） | 访问静态内容（httpStatic）的认证用户名 |
| `http_static.password` | 密码（默认空） | 访问静态内容的认证密码 |
| `ssl` | 布尔值（默认 `true`） | 是否在 Web 界面上启用 SSL（HTTPS），仅对直接访问生效，不影响 Ingress |
| `certfile` | 字符串（默认 `fullchain.pem`） | SSL 证书文件，必须存放在 `/ssl/` 目录下 |
| `keyfile` | 字符串（默认 `privkey.pem`） | SSL 私钥文件，必须存放在 `/ssl/` 目录下 |
| `system_packages` | 字符串数组（默认 `[]`） | 需要额外安装的 Alpine 系统包，如 `g++`、`make`、`ffmpeg` |
| `npm_packages` | 字符串数组（默认 `[]`） | 需要额外安装的 NPM 包或 Node-RED 节点，如 `node-red-dashboard`、`node-red-contrib-ccu` |
| `init_commands` | 字符串数组（默认 `[]`） | 每次启动加载项时执行的 Shell 命令 |
| `safe_mode` | 布尔值（可选） | 设为 `true` 时以 `--safe` 标志启动，不加载任何流程，用于故障排查 |
| `leave_front_door_open` | 布尔值（可选） | 设为 `true` 并留空用户名/密码可关闭认证。强烈不建议开启，风险自负 |
| `max_old_space_size` | 整数（可选，单位 MB） | 设置 Node.js V8 老生代内存上限，接近上限时 V8 会花更多时间做垃圾回收 |

## 使用 / 访问入口

- **Web 界面**：可通过 Home Assistant 侧边栏的加载项入口（Ingress）直接访问；也支持直接访问模式（`http://<你的HA地址>:1880`）。
- **首次使用**：安装并启动后点击「OPEN WEB UI」即可进入 Node-RED 编辑器，创建并部署你的第一个流程。
- **集成 Home Assistant**：加载项已启用 Home Assistant API，可直接拖入 Home Assistant 相关节点使用。
- **配置目录**：大部分配置保存在加载项配置目录中，包括 `flows.json`。
- **时区**：默认跟随 Home Assistant 设置中的时区；如需单独覆盖，可在 `settings.js` 的 `module.exports = {` 前添加 `process.env.TZ = "你的时区";` 并重启加载项。

## 常见问题

- **无法访问 HTTP 节点或 Node-RED Dashboard？** 需要在加载项的「网络（Network）」配置中设置端口号以启用直接访问模式；同时确认 URL 以 `/endpoint/` 开头，否则会触发 Home Assistant 认证。
- **更新后日志报 `Unauthorized WebSocket access!`？** 请检查 Node-RED 中 Home Assistant 服务器配置：双击任意 Home Assistant 节点，点击服务器名旁的小铅笔图标，确认已勾选「I use the Home Assistant App」。

---
- 英文原版：Home Assistant Community App: Node-RED；链接 https://github.com/hassio-addons/repository/blob/master/node-red/README.md
- 来源仓库：frenck
