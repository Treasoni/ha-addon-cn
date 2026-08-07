<!-- zh-guide -->
# chromium

## 简介

Chromium 是一款面向 PC、Mac 和移动端的快速、隐私且安全的网页浏览器。本 add-on 基于 linuxserver 的 docker-chromium 镜像，将 Chromium 浏览器运行在 Home Assistant 中，可通过 Ingress 在侧边栏直接使用。

## 安装

1. 在 Home Assistant → 设置 → 加载项 → 商店，添加本商店仓库：
   - Gitee：https://gitee.com/zhqznc_10603234_123/ha-addon
   - GitHub：https://github.com/Treasoni/ha-addon-cn
2. 搜索 `browser_chromium` 并安装。
3. 安装完成后启动 add-on，点击「保存」并设置你的偏好选项，然后查看日志确认运行正常。

## 配置

| 配置键 | 类型 / 默认值 | 说明 |
| --- | --- | --- |
| `env_vars` | 列表 / 空 | 传入容器的额外环境变量（`name`/`value` 形式） |
| `DNS_server` | 字符串 / 默认 `8.8.8.8` | 自定义 DNS 服务器，留空使用路由器 DNS |
| `PUID` | 整数 / 默认 `0` | 运行用户的用户 ID |
| `PGID` | 整数 / 默认 `0` | 运行用户的组 ID |
| `certfile` | 字符串 / 默认 `fullchain.pem` | 自定义证书文件名（位于 /ssl） |
| `keyfile` | 字符串 / 默认 `privkey.pem` | 自定义证书私钥文件名（位于 /ssl） |
| `use_own_certs` | 布尔 / 默认 `false` | 是否使用自定义证书 |
| `additional_apps` | 字符串（可选） / 空 | 额外安装的应用，如 `engrampa,thunderbird`（应用不持久，需在选项中安装） |
| `DRINODE` | 枚举（GPU 设备） / 默认 `/dev/dri/renderD128` | 指定图形设备，图形不工作时使用此项选择设备 |
| `KEYBOARD` | 枚举（键盘布局） / 空 | 键盘布局，如 `en-us-qwerty` |
| `PASSWORD` | 字符串（可选） / 空 | 访问界面时所需的密码 |
| `TZ` | 字符串（可选） / 空 | 时区，如 `Europe/London` |

## 使用 / 访问入口

启动后可在 Home Assistant 侧边栏看到 chromium 图标，点击进入。Web 界面（HTTP）容器端口 3000/tcp 默认映射到宿主端口 3000，HTTPS 界面端口 3001/tcp 映射到宿主端口 3001；Chrome 调试端口 9221/tcp 默认禁用。

## 常见问题

- 默认基于 `abc` 用户，默认密码为 `abc`；如需设置密码，可在容器内的图形终端执行 `passwd`，然后通过 `http://localhost:3000/?login=true` 访问界面。
- 应用安装不持久，需要通过 add-on 选项安装；但应用的配置会保留。
- 如果图形界面不工作，使用 `DRINODE` 选项指定图形设备。
- 可参考 linuxserver 文档查看所有可选的环境变量。

---
- 英文原版：[Home assistant add-on: chromium](https://github.com/alexbelgium/hassio-addons/blob/master/chromium/README.md)
- 来源仓库：alexbelgium
