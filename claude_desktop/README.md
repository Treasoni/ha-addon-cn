<!-- zh-guide -->
# Claude Desktop

## 简介

在 LinuxServer.io Selkies add-on 中运行 Claude Desktop，并默认集成 Headroom 上下文压缩、RTK Bash 输出加速与 TokenSave 语义代码智能。本 add-on 以 Home Assistant Ingress 提供 Claude Desktop 的 Web 界面，内置 Claude Code，支持通过 MCP 服务器、权限策略、Home Assistant MCP 桥与可选的 Codex CLI 进行扩展。

## 安装

1. 在 Home Assistant → 设置 → 加载项 → 商店，添加本商店仓库：
   - Gitee：https://gitee.com/zhqznc_10603234_123/ha-addon
   - GitHub：https://github.com/Treasoni/ha-addon-cn
2. 搜索 `claude_desktop` 并安装。
3. 安装完成后启动 add-on，并从侧边栏打开 Web 界面。
4. 使用支持 Desktop 应用的 claude.ai 套餐账户登录（不接受 API 密钥）。

## 配置

| 配置键 | 类型 / 默认值 | 说明 |
| --- | --- | --- |
| `env_vars` | 列表 / 空 | 传入容器的额外环境变量（`name`/`value` 形式） |
| `DNS_server` | 字符串 / 默认 `8.8.8.8` | 容器使用的 DNS 服务器 |
| `PUID` | 整数 / 默认 `1000` | 运行 Claude Desktop 的共享 abc 桌面账户的用户 ID |
| `PGID` | 整数 / 默认 `1000` | 运行 Claude Desktop 的共享 abc 桌面账户的组 ID |
| `TZ` | 字符串（可选） / 空 | 时区，如 `Europe/Brussels` |
| `KEYBOARD` | 枚举（键盘布局） / 空 | Selkies 键盘布局 |
| `PASSWORD` | 字符串（可选） / 空 | 直连 Selkies 端口时的可选密码 |
| `DRINODE` | 枚举（GPU 设备） / 空 | Selkies 的可选 GPU 设备覆盖 |
| `MAX_RES` | 字符串（可选） / 空 | 虚拟屏幕上限制，格式 `WIDTHxHEIGHT`（如 15360x8640） |
| `data_location` | 字符串 / 默认 `/data/data` | Claude 与工具的持久化主目录，跨重启保留 |
| `additional_apps` | 字符串 / 空 | 启动时安装的 Debian apt 包（逗号分隔） |
| `additional_pip` | 字符串 / 空 | 启动时通过 `uv` 安装的 pip 包（逗号分隔） |
| `github_email` | 字符串 / 空 | 全局 Git 作者邮箱 |
| `enable_ha_mcp` | 布尔 / 默认 `false` | 在 Claude 中注册 Home Assistant MCP 服务（需 `ha_mcp_token`） |
| `ha_mcp_url` | 字符串 / 默认 `http://homeassistant:8123/api/mcp` | Home Assistant MCP Server 集成的 Streamable HTTP 端点 |
| `ha_mcp_token` | 密码 / 空 | MCP 桥使用的 Home Assistant 长效访问令牌 |
| `enable_ha_api_helper` | 布尔 / 默认 `true` | 提供 `ha-cli` Core API 辅助，让 Claude 无需挂载 `/config` 即可配置 Home Assistant |
| `github_token` | 密码 / 空 | 用于认证 `gh` 与 Git 操作的 GitHub 令牌 |
| `github_username` | 字符串 / 空 | 全局 Git 作者名 |
| `enable_tools_health_report` | 布尔 / 默认 `true` | 每小时向 add-on 日志写入 Headroom/RTK/TokenSave 的独立节省报告 |
| `expose_headroom_dashboard` | 布尔 / 默认 `false` | 将 Headroom 绑定到所有接口；需同时手动映射 8787/tcp |
| `headroom_auto_compress` | 布尔 / 默认 `true` | 通过受管的 PostToolUse hook 自动压缩大体积工具输出 |
| `headroom_wrap_claude_code` | 布尔 / 默认 `true` | 让基于 PATH 的 Claude Code 启动走已运行的 Headroom 代理 |
| `install_caveman` | 布尔 / 默认 `false` | 启动时安装第三方 Caveman Claude Code 插件 |
| `install_codex_cli` | 布尔 / 默认 `false` | 启动时安装最新稳定版 OpenAI Codex CLI 并注册其原生 MCP 服务 |
| `codex_sandbox_mode` | 枚举 / 默认 `workspace-write` | Codex 的文件系统范围：`read-only` / `workspace-write` / `danger-full-access` |
| `install_github_cli` | 布尔 / 默认 `true` | 对内置 `git` 与 `gh` 命令进行安装检查 |
| `install_headroom` | 布尔 / 默认 `true` | 注册 Headroom MCP 并运行受管的本地代理 |
| `install_rtk` | 布尔 / 默认 `true` | 配置 RTK 的 Claude Code PreToolUse Bash hook |
| `install_tokensave` | 布尔 / 默认 `true` | 安装 TokenSave 完整的全局 Claude 集成 |
| `mcp_servers_desktop` | 列表 / 默认全部（headroom、tokensave、homeassistant、codex） | Claude Desktop 注册的受管 MCP 服务 |
| `mcp_servers_code` | 列表 / 默认全部（headroom、tokensave、homeassistant、codex） | Claude Code 注册的受管 MCP 服务 |
| `permission_mode` | 枚举 / 默认 `auto` | Claude Code 权限策略：`strict` / `auto` / `bypass` |
| `tokensave_project_paths` | 列表 / 空 | 启动时初始化或同步的显式 Git 仓库绝对路径 |

## 使用 / 访问入口

启动后可在 Home Assistant 侧边栏看到 Claude Desktop 图标，点击进入。登录需使用支持 Desktop 应用的 claude.ai 套餐账户（不接受 API 密钥）。可选端口 3001/tcp（Claude Desktop Web 界面）与 8787/tcp（Headroom 仪表盘）默认禁用，需在 add-on 的「网络」设置中手动映射后使用。

## 常见问题

- Claude Desktop 登录需要支持 Desktop 应用的 claude.ai 套餐；API 密钥不被 Desktop 应用接受。Anthropic 的 Linux 测试版目前不包含 Computer Use 或语音输入。
- 当 `permission_mode` 设为 `bypass` 且 `PUID` 为 0 时，add-on 会在启动前自动回退到 UID 1000，因为 Claude Code 拒绝在 root UID 下使用 bypass 模式。
- 登录状态与权限授权通过内置的 gnome-keyring 在重启后持久保留。
- 持久化状态位于 `data_location`（默认 `/data/data`）：Claude Desktop 登录（`~/.config/Claude`）、Claude Code 配置（`~/.claude`）、Codex 认证（`~/.codex`）等。
- 可在容器内运行 `claude-tools-doctor.sh` 进行诊断，检查二进制、路由、hook、MCP 注册、代理健康与权限等信息。

---
- 英文原版：[Home assistant add-on: Claude Desktop](https://github.com/alexbelgium/hassio-addons/blob/master/claude_desktop/README.md)
- 来源仓库：alexbelgium
