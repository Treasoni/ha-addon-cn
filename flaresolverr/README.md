<!-- zh-guide -->
# FlareSolverr

## 简介

FlareSolverr 是一个用于绕过 Cloudflare 人机验证的代理服务器。它平时以低资源占用空闲等待请求，收到请求后通过 Puppeteer 无头浏览器（Firefox）自动完成 Cloudflare 验证，从而让后续请求可以正常访问受保护的网站。

## 安装

1. 在 Home Assistant → 设置 → 加载项 → 商店，添加本商店仓库：
   - Gitee：https://gitee.com/zhqznc_10603234_123/ha-addon
   - GitHub：https://github.com/Treasoni/ha-addon-cn
2. 搜索 FlareSolverr 并安装。

## 配置

本加载项默认开箱即用，无需任何配置。仅有一个可选配置项：

| 配置键 | 类型/默认值 | 说明 |
| --- | --- | --- |
| env_vars | 数组，默认 `[]` | 自定义环境变量列表。每个条目包含 `name`（须匹配 `^[A-Za-z0-9_]+$`，即大小写字母、数字、下划线）与 `value`（字符串，可为空）。用于向 FlareSolverr 传递额外的环境变量。 |

## 使用 / 访问入口

- 本加载项没有 Ingress 入口，通过 Web 界面访问，默认端口为 8191。
- 启动后可在加载项页面点击"打开 Web UI"，或直接访问 http://homeassistant:8191。
- FlareSolverr 提供 REST API，端点地址为 http://homeassistant:8191/v1。示例请求：

```json
{
  "cmd": "request.get",
  "url": "https://example.com",
  "maxTimeout": 60000
}
```

- 与 *arr 系列应用集成：
  - Prowlarr / Jackett：将 FlareSolverr URL 设置为 http://homeassistant:8191。
  - Sonarr / Radarr：在索引器配置中使用 FlareSolverr 代理。

## 常见问题

- 浏览器会占用较多内存，在内存有限的设备上请避免同时发起大量并发请求（README 建议 512MB+ 内存）。
- 官方建议至少 2 核 CPU、4 GB 内存，否则系统可能卡顿或崩溃。
- 使用本加载项需要设备能正常访问互联网。

---
- 英文原版：Home assistant add-on: Flaresolver；链接 https://github.com/alexbelgium/hassio-addons/blob/master/flaresolverr/README.md
- 来源仓库：alexbelgium
