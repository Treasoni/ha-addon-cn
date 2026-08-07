<!-- zh-guide -->
# Changedetection.io

## 简介
Changedetection.io 是一个免费开源的自建网页监控工具，用于监控网页内容变化、发送通知并进行变更检测。本加载项基于 linuxserver.io 的 Docker 镜像构建，可通过 Home Assistant 的 Ingress 或独立端口访问 Web 界面。

## 安装
1. 在 Home Assistant → 设置 → 加载项 → 商店，添加本商店仓库：
   - Gitee：https://gitee.com/zhqznc_10603234_123/homeassistant
   - GitHub：https://github.com/Treasoni/ha-addon-cn
2. 搜索 changedetection.io 并安装。

## 配置
安装后点击「配置」标签页，可按需修改以下选项（默认配置即可使用）：

| 配置键 | 类型/默认值 | 说明 |
|--------|------------|------|
| `PUID` | int / `0` | 文件权限的用户 ID |
| `PGID` | int / `0` | 文件权限的组 ID |
| `TIMEOUT` | int / `60000` | 请求超时时间（毫秒） |
| `TZ` | str / 空 | 时区，例如 `Europe/London` |
| `BASE_URL` | str / 空 | 反向代理后面的完整访问 URL |
| `PLAYWRIGHT_DRIVER_URL` | str / 空 | Playwright 驱动的 WebSocket URL |
| `env_vars` | list / `[]` | 追加的额外环境变量列表（变量名/值），变量名需匹配 `^[A-Za-z0-9_]+$` |

## 使用 / 访问入口
- **Ingress（推荐）**：加载项支持 Ingress，可在 Home Assistant 侧边栏或加载项页面直接打开 Web 界面。
- **独立端口**：Web 界面默认监听 `5000` 端口，访问地址为 `http://<你的设备IP>:5000`（使用 Ingress 时该端口非必需）。
- **首次使用**：安装并启动加载项后，打开 Web 界面即可创建你的第一个监控任务，添加要监控的网页 URL。
- **侧边栏快捷方式**：在 设置 → 仪表盘 中添加「网页」类型面板，粘贴加载项页面显示的 Web UI 地址，填写标题、图标（建议 `mdi:vector-difference`）及相对路径（例如 `change-detection`）即可。
- **数据目录**：配置数据保存在 `/config/addons_config/changedetection.io`。

## 常见问题
- **如何监控需要浏览器渲染的动态页面？** 安装并启动 Browserless Chrome 加载项，将其在界面中显示的 WebSocket 地址填入 `PLAYWRIGHT_DRIVER_URL`（形如 `ws://db21ed7f-browserless-chrome:3000/chromium?headless=true&stealth=true&blockAds=true`），然后重启本加载项，即可在监控任务中使用浏览器选项。
- **需要额外环境变量怎么办？** 使用配置中的 `env_vars` 选项以「变量名/值」的形式传入，变量名不区分大小写。
- **加载项页面打不开？** 检查加载项日志确认启动是否正常；若配置了反向代理，请在 `BASE_URL` 中填写正确的完整访问地址。

---
- 英文原版：Home assistant add-on: changedetection.io；链接 https://github.com/alexbelgium/hassio-addons/blob/master/changedetection.io/README.md
- 来源仓库：alexbelgium
