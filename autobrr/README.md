<!-- zh-guide -->
# Autobrr

## 简介

Autobrr 是一款现代化的 BT（torrent）下载自动化工具，灵感与思路来自 trackarr、autodl-irssi 和 flexget 等工具，集成了 RSS 订阅监控、下载客户端对接与自动化规则/过滤器等能力。它基于 [autobrr/autobrr](https://github.com/autobrr/autobrr) 镜像构建。

## 安装

1. 在 Home Assistant → 设置 → 加载项 → 商店，添加本商店仓库：
   - Gitee：https://gitee.com/zhqznc_10603234_123/ha-addon
   - GitHub：https://github.com/Treasoni/ha-addon-cn
2. 搜索 autobrr 并安装。
3. 按偏好设置加载项选项，保存并启动，然后打开 Web 界面调整软件设置。

## 配置

| 配置键 | 类型 / 默认值 | 说明 |
| ------ | ----------- | ---- |
| `PGID` | 整数，默认 `0` | 文件权限组 ID（Group ID），用于文件权限 |
| `PUID` | 整数，默认 `0` | 文件权限用户 ID（User ID），用于文件权限 |
| `env_vars` | 列表，默认空 | 附加环境变量，通过此选项传入额外环境变量（变量名大小写均可） |
| `TZ` | 可选字符串，默认空 | 时区，例如 `Europe/London` |
| `localdisks` | 可选字符串，默认空 | 要挂载的本地磁盘，例如 `sda1,sdb1` |
| `networkdisks` | 可选字符串，默认空 | 要挂载的 SMB 网络共享，例如 `//192.168.1.100/downloads` |
| `cifsusername` | 可选字符串，默认空 | SMB 网络共享的用户名 |
| `cifspassword` | 可选字符串，默认空 | SMB 网络共享的密码 |
| `cifsdomain` | 可选字符串，默认空 | SMB 网络共享的域名/工作组 |

## 使用 / 访问入口

- **侧边栏**：加载项支持 Ingress，启动后可在 Home Assistant 侧边栏看到 Autobrr 图标，点击进入。
- **Web 界面**：也可通过 http://homeassistant:7474 访问（容器端口 `7474/tcp` 映射到宿主端口 `7474`）。
- **首次登录**：默认账号为 `admin`，密码为 `password`，首次登录后请立即修改。

## 常见问题

- **默认密码是什么？** 默认账号 `admin` / 密码 `password`，首次登录后请务必修改。
- **挂载本地磁盘/网络共享不生效？** `localdisks` 用于挂载本地磁盘（如 `sda1,sdb1`），`networkdisks` 用于挂载 SMB 共享并配合 `cifsusername`/`cifspassword`/`cifsdomain` 使用，参见上游关于挂载磁盘的说明。
- **文件权限不对？** 通过调整 `PUID`/`PGID` 为本地用户 ID/组 ID 来匹配文件权限。
- **如何开始使用？** 打开 Web 界面后，先修改登录凭据，再配置 RSS 索引源与下载客户端，然后设置自动化规则和过滤器，可用示例发布进行测试。

---
- 英文原版：Home assistant add-on: Autobrr；链接 https://github.com/alexbelgium/hassio-addons/blob/master/autobrr/README.md
- 来源仓库：alexbelgium
