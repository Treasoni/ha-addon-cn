<!-- zh-guide -->
# The Lounge

## 简介

The Lounge 是一款自托管的 Web IRC 客户端，采用现代简洁的界面，支持主题定制、推送通知、链接预览、文件上传等功能，完全跨平台且适配移动端。

## 安装

1. 在 Home Assistant 中进入「设置 → 加载项 → 商店」，点击右上角菜单添加本商店仓库：
   - Gitee：https://gitee.com/zhqznc_10603234_123/ha-addon
   - GitHub：https://github.com/Treasoni/ha-addon-cn
2. 在商店中搜索 `thelounge`（The Lounge）并点击安装。
3. 在配置中添加用户并启动加载项，登录后请尽快修改默认密码。

## 配置

> 注意：修改配置后需重启加载项才会生效。

| 配置键 | 类型 / 默认值 | 说明 |
| --- | --- | --- |
| `log_level` | 枚举（trace\|debug\|info\|notice\|warning\|error\|fatal），可选 / 空 | 加载项的日志输出级别。`trace` 显示全部细节，`debug` 显示详细调试信息，`info` 为正常事件，`warning` 为非错误的异常，`error` 为无需立即处理的错误，`fatal` 为致命错误。推荐使用 `info`。 |
| `ssl` | 布尔 / true | 是否在应用上启用 SSL（HTTPS）。设为 `true` 启用，`false` 禁用。 |
| `certfile` | 字符串 / fullchain.pem | 用于 SSL 的证书文件，必须存放在 `/ssl/` 目录下。 |
| `keyfile` | 字符串 / privkey.pem | 用于 SSL 的私钥文件，必须存放在 `/ssl/` 目录下。 |
| `default_theme` | 字符串 / default | 每个用户的默认主题。预装主题为 `default` 和 `morning`，可通过下文的 `themes` 选项安装更多。用户仍可在应用设置中更改主题。 |
| `themes` | 字符串列表 / [thelounge-theme-solarized] | 需要安装的主题列表，主题可从 npm 注册表中获取，填写包名即可。 |
| `users` | 字符串列表 / 空 | 需要创建的用户列表。初始默认密码为 `hassio`，登录后请务必立即修改密码。 |

## 使用 / 访问入口

启动后可在 Home Assistant 侧边栏看到 The Lounge 图标，点击进入即可打开 IRC 客户端界面。

## 常见问题

- **首次登录密码**：新建用户的初始默认密码为 `hassio`，请务必在登录后第一时间修改。
- **主题选择**：预装主题为 `default` 和 `morning`；如需更多主题，在 `themes` 中填写 npm 包名并重启加载项。
- **适用架构**：本加载项支持 aarch64、amd64，已停止对 armv7 的支持。

---
- 英文原版：The Lounge；链接 https://github.com/hassio-addons/repository/blob/main/thelounge/README.md
- 来源仓库：frenck
