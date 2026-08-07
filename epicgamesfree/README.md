<!-- zh-guide -->
# Epic Games Free

## 简介
Epic Games Free 基于 claabs/epicgames-freegames-node，用于自动登录 Epic Games 商店并领取每周免费游戏，支持多账户、两步验证（TOTP）、验证码通知与定时运行。本加载项基于 charlocharlie/epicgames-freegames 的 Docker 镜像构建。

## 安装
1. 在 Home Assistant → 设置 → 加载项 → 商店，添加本商店仓库：
   - Gitee：https://gitee.com/zhqznc_10603234_123/ha-addon
   - GitHub：https://github.com/Treasoni/ha-addon-cn
2. 搜索 epicgamesfree 并安装。

## 配置
大部分应用配置通过 JSON 文件完成，存放于 `/config/addons_config/epicgamesfree/`（首次启动自动生成默认值）：`config.json` 为主配置文件，`cookies.json` 为可选的身份 Cookie。加载项本身提供以下选项：

| 配置键 | 类型 / 默认值 | 说明 |
|--------|---------------|------|
| `disable_cron` | 布尔 / `false` | 关闭内置 cron 定时服务（当使用外部调度器时开启） |
| `env_vars` | 列表 / 空 | 额外环境变量（大写或小写命名）；列表项含 `name`（环境变量名，须匹配 `^[A-Za-z0-9_]+$`）与 `value`（环境变量值，可选） |

在 `config.json` 中可配置 `accounts`（Epic 账户列表，含 email/password/totp）、`cronSchedule`（默认 `0 */6 * * *`）、`runOnStartup`、`logLevel`、`webPortalConfig.baseUrl`（Web 门户基础地址）以及 `notifiers`（邮件、Discord、Telegram、Apprise 等通知目标）。

## 使用 / 访问入口
本加载项未启用 Ingress，通过端口访问：容器端口 `3000/tcp` 映射到宿主端口 `3000`，浏览器访问 http://homeassistant:3000 打开 Web 门户。

## 常见问题
1. 由于 Epic 加强了对自动化行为的检测，现已无法自动领取游戏；加载项会通过你配置的通知方式发送兑换链接，由你手动点击完成兑换。
2. 支持配置多个 Epic 账户；开启了两步验证的账户可填写 TOTP 密钥。
3. 遇到登录问题时，请先核对凭据是否正确，再检查 2FA/TOTP 配置，必要时可在 `cookies.json` 中导入浏览器 Cookie。
4. 出现超时错误时，可在 `config.json` 中增加 `browserNavigationTimeout: 300000` 后重启加载项。
5. 升级时若只有旧版 config.yaml 而无 config.json，加载项会重建默认 config.json，保证配置可用。

---
- 英文原版：Home assistant add-on: Epic Games Free；链接 https://github.com/alexbelgium/hassio-addons/blob/master/epicgamesfree/README.md
- 来源仓库：alexbelgium
