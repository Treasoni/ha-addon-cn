<!-- zh-guide -->
# Nginx Proxy Manager

## 简介
Nginx Proxy Manager（NPM）让你用简单而强大的图形界面管理 Nginx 反向代理主机。即使不熟悉 Nginx 或 Let's Encrypt，也能把入站连接转发到任何地方，并免费获得 SSL 证书。它还可以为网站启用用户名/密码认证，高级用户还能为每个主机自定义额外的 Nginx 配置指令。

## 安装
1. 在 Home Assistant → 设置 → 加载项 → 商店，添加本商店仓库：
   - Gitee：https://gitee.com/zhqznc_10603234_123/homeassistant
   - GitHub：https://github.com/Treasoni/ha-addon-cn
2. 搜索 nginxproxymanager 并安装。

## 配置
本加载项不提供任何配置项（config.yaml 中没有定义 options/schema），安装后即可直接使用。

## 使用 / 访问入口
- 首次访问：点击「打开 Web UI」，使用默认账号 `admin@example.com`、默认密码 `changeme` 登录。
- 管理界面端口：`81`（Nginx Proxy Manager 管理 Web 界面，即 Web UI 入口）。
- 对外端口：`80`（HTTP 入口）、`443`（HTTPS/SSL 入口）。
- 常用操作：
  - 将你的域名转发到 Home Assistant、其他加载项，或家里/任意位置运行的网站。
  - 为网站启用用户名/密码认证，创建可访问该应用的账号列表。
  - 高级用户可通过额外的 Nginx 配置指令，自定义每个代理主机的行为。
- 需要把路由器上的端口 `443`（可选加 `80`）转发到运行 Home Assistant 的机器，外部才能通过 HTTPS 访问你的服务。

## 常见问题
- 如何登录管理界面？安装并启动后点击「打开 Web UI」，使用默认账号 `admin@example.com`、密码 `changeme` 登录，登录后建议尽快修改默认密码。
- 会占用哪些端口？`80`（HTTP 入口）、`81`（管理界面）、`443`（HTTPS/SSL 入口），若与本机其他服务冲突请调整端口映射。

---
- 英文原版：Home Assistant Community Add-on: Nginx Proxy Manager；链接 https://github.com/hassio-addons/repository/blob/master/nginxproxymanager/README.md
- 来源仓库：frenck
