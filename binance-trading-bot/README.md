<!-- zh-guide -->
# Binance Trading Bot

## 简介

Binance Trading Bot 是一个自动化的 Binance 加密货币交易机器人，支持同时交易多种加密货币，通过网格交易（Grid Trading）实现低买高卖，并集成了 TradingView 技术分析信号。它基于 [chrisleekr/binance-trading-bot](https://github.com/chrisleekr/binance-trading-bot) 构建。**请注意：这是一个测试性质的应用，请勿使用真实资金运行实盘模式。**

## 安装

1. 在 Home Assistant → 设置 → 加载项 → 商店，添加本商店仓库：
   - Gitee：https://gitee.com/zhqznc_10603234_123/ha-addon
   - GitHub：https://github.com/Treasoni/ha-addon-cn
2. 搜索 binance-trading-bot 并安装。
3. 按你的偏好仔细配置加载项选项（尤其是 API 密钥与交易模式），保存并启动。

## 配置

| 配置键 | 类型 / 默认值 | 说明 |
| ------ | ----------- | ---- |
| `BINANCE_MODE` | 枚举 `live\|test`，默认 `test` | 交易模式：`test` 使用 Binance 测试网（模拟盘），`live` 为实盘；实盘存在风险，请谨慎使用 |
| `BINANCE_AUTHENTICATION_ENABLED` | 布尔，默认开启 | 是否启用 Web 界面的登录认证 |
| `BINANCE_AUTHENTICATION_PASSWORD` | 字符串，默认空 | Web 界面登录密码，启用认证时必填 |
| `BINANCE_SLACK_ENABLED` | 布尔，默认关闭 | 是否启用 Slack 通知 |
| `BINANCE_SLACK_WEBHOOK_URL` | 可选字符串，默认空 | Slack 的 Incoming Webhook 地址 |
| `BINANCE_SLACK_CHANNEL` | 可选字符串，默认空 | 接收通知的 Slack 频道 |
| `BINANCE_SLACK_USERNAME` | 可选字符串，默认空 | Slack 通知显示的用户名 |
| `BINANCE_TEST_API_KEY` | 可选字符串，默认空 | Binance 测试网（testnet）API 密钥 |
| `BINANCE_TEST_SECRET_KEY` | 可选字符串，默认空 | Binance 测试网 API 私钥 |
| `BINANCE_LIVE_API_KEY` | 可选字符串，默认空 | Binance 实盘 API 密钥 |
| `BINANCE_LIVE_SECRET_KEY` | 可选字符串，默认空 | Binance 实盘 API 私钥 |
| `BINANCE_LOCAL_TUNNEL_ENABLED` | 可选布尔，默认空 | 是否启用本地隧道，用于外部远程访问 |
| `BINANCE_LOCAL_TUNNEL_SUBDOMAIN` | 可选字符串，默认空 | 本地隧道使用的子域名 |
| `env_vars` | 列表，默认空 | 附加环境变量，通过此选项传入额外环境变量（变量名大小写均可） |

> 说明：更完整的配置说明请参见上游项目 https://github.com/chrisleekr/binance-trading-bot 。机器人依赖本地 Redis（环境变量 `BINANCE_REDIS_HOST`/`BINANCE_REDIS_PORT`）。

## 使用 / 访问入口

- **侧边栏**：加载项支持 Ingress，启动后可在 Home Assistant 侧边栏看到 Binance Trading Bot 图标，点击进入。
- **直接访问**：Web 界面为 http://homeassistant:80（容器端口 `80/tcp`）；TradingView 信号集成使用端口 8080（容器端口 `8080/tcp`）。
- **首次使用**：先在 `test` 模式下用测试网 API 密钥验证流程，确认无误后再考虑实盘。

## 常见问题

- **可以用真实资金吗？** 上游明确标注这是测试应用，**请勿使用真实资金**运行；默认模式为 `test`（模拟盘）。
- **如何接入 Binance？** 在 Binance 后台创建 API 密钥，将密钥填入 `BINANCE_TEST_API_KEY`/`BINANCE_TEST_SECRET_KEY`（测试网）或 `BINANCE_LIVE_API_KEY`/`BINANCE_LIVE_SECRET_KEY`（实盘）。
- **登录被拒绝？** 确认已启用 `BINANCE_AUTHENTICATION_ENABLED` 并正确设置 `BINANCE_AUTHENTICATION_PASSWORD`。
- **如何接收通知？** 启用 `BINANCE_SLACK_ENABLED` 并填写 `BINANCE_SLACK_WEBHOOK_URL` 即可通过 Slack 接收交易通知。

---
- 英文原版：Home assistant add-on: Binance Trading Bot (do not use with real money!)；链接 https://github.com/alexbelgium/hassio-addons/blob/master/binance-trading-bot/README.md
- 来源仓库：alexbelgium
