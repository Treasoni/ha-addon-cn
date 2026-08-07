<!-- zh-guide -->
# Webtrees

## 简介

webtrees 是 Web 上领先的在线协作式家谱（系谱学）应用，支持多人共同维护与查阅家族历史、族谱树等信息。本加载项基于 NathanVaughn/webtrees-docker 镜像构建。

## 安装

1. 在 Home Assistant → 设置 → 加载项 → 商店，添加本商店仓库：
   - Gitee：https://gitee.com/zhqznc_10603234_123/ha-addon
   - GitHub：https://github.com/Treasoni/ha-addon-cn
2. 搜索 webtrees 并安装。

## 配置

修改配置后需要重启加载项才能生效。可选配置键如下：

| 配置键 | 类型/默认值 | 说明 |
| ------ | ----------- | ---- |
| `env_vars` | 列表，默认空 | 传入容器的自定义环境变量列表，每项包含 `name`（变量名，须匹配 `^[A-Za-z0-9_]+$`）与 `value`（变量值，可选）。 |
| `BASE_URL` | 字符串（URL），默认 `http://192.168.178.23` | 访问 webtrees 时使用的地址，请改为你的实际访问地址。 |
| `DATA_LOCATION` | 字符串，默认 `/config/data` | 数据存放目录。 |
| `certfile` | 字符串，默认 `fullchain.pem` | TLS 证书文件，需存放在 `/ssl/` 目录。 |
| `keyfile` | 字符串，默认 `privkey.pem` | TLS 私钥文件，需存放在 `/ssl/` 目录。 |
| `ssl` | 布尔，默认 `false` | 是否启用 HTTPS。 |
| `base_url_portless` | 可选布尔，默认空 | 是否使用不带端口的 base URL（例如经 Cloudflare 隧道反向代理时需启用）。 |
| `trusted_headers` | 可选字符串，默认空 | 受信任的来源地址或 CIDR 网段，用于反向代理场景。 |
| `cifsdomain` | 可选字符串，默认空 | 网络共享（SMB）的域/工作组。 |
| `cifspassword` | 可选字符串，默认空 | 网络共享（SMB）的密码。 |
| `cifsusername` | 可选字符串，默认空 | 网络共享（SMB）的用户名。 |
| `localdisks` | 可选字符串，默认空 | 需要挂载的本地磁盘，例如 `sda1,sdb1`。 |
| `networkdisks` | 可选字符串，默认空 | 需要挂载的 SMB 网络共享，例如 `//SERVER/SHARE`。 |

## 使用 / 访问入口

本加载项不提供 Ingress，通过端口访问：

- Web 界面容器端口 `80/tcp`，宿主端口 9999。
- HTTPS 容器端口 `443/tcp` 默认关闭（宿主映射未启用），启用 SSL 后使用。

首次启动会进入初始化向导，管理员账号与密码在向导中设置，请留意加载项「日志」中的提示。

## 常见问题

- **首次如何创建管理员？** 首次启动会打开初始化向导并创建第一个用户，向导说明见加载项日志。从 2.2.1-4 起不再自动创建首个用户，升级前请务必先在 webtrees 界面做好备份。
- **如何更换数据库？** 数据库类型（sqlite/mysql/psql）在首次启动向导中选择；如需更换，可手动修改 `/config/data` 目录下的 `config.php.ini` 文件（第三方工具可经 `/addon_configs/xxx-webtrees/data` 访问）。
- **自定义模块安装失败？** 2.2.6.1 修复了从 webtrees 界面安装自定义模块（如 Custom Module Manager 插件）失败的问题（`/config/modules_v4` 目录权限）。若仍失败，请检查该目录的属主与权限是否与运行用户一致。
- **如何让家人从外网访问？** 可通过 Cloudflare 隧道等方式免费、安全地对外暴露。此时 webtrees 的 `BASE_URL` 需使用 https 协议的外部访问域名、`ssl` 关闭（由 Cloudflare 负责）、`base_url_portless` 设为 `true`；Cloudflared 的 service 指向 `你的HA地址:9999`。
- **需要自定义环境变量？** 通过 `env_vars` 选项传入；也支持通过配置引用 config.yaml 添加更多环境变量（须为合法 YAML 格式，启动时校验）。
- Home Assistant 项目已弃用 armv7、armhf 与 i386 架构支持，将在 Home Assistant 2025.12 版本中完全移除。

---
- 英文原版：Home assistant add-on: Webtrees；链接 https://github.com/alexbelgium/hassio-addons/blob/master/webtrees/README.md
- 来源仓库：alexbelgium
