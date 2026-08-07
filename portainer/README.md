<!-- zh-guide -->
# Portainer

## 简介
Portainer 是一个开源、轻量的 Docker 管理界面，帮助你轻松管理 Docker 主机或 Docker Swarm 集群。它提供详细的 Docker 概览，让你直观地管理容器、镜像、网络和数据卷，让 Docker 管理变得前所未有的简单。

## 安装
1. 在 Home Assistant → 设置 → 加载项 → 商店，添加本商店仓库：
   - Gitee：https://gitee.com/zhqznc_10603234_123/homeassistant
   - GitHub：https://github.com/Treasoni/ha-addon-cn
2. 搜索 portainer 并安装。

## 配置
| 配置键 | 类型 / 默认值 | 说明 |
|--------|---------------|------|
| `ssl` | bool / `false` | 为 Web 界面启用 HTTPS |
| `certfile` | str / `fullchain.pem` | SSL 证书文件（位于 `/ssl/` 目录） |
| `keyfile` | str / `privkey.pem` | SSL 私钥文件（位于 `/ssl/` 目录） |
| `password` | str / `homeassistant` | 管理员密码（至少 12 个字符；设置为 `empty` 或留空可进入初始化/恢复流程） |
| `env_vars` | array / `[]` | 传递给容器的附加环境变量（名称需匹配 `^[A-Za-z0-9_]+$`） |

## 使用 / 访问入口
- 通过侧边栏 Ingress 直接访问（免记端口）。
- 也可通过 Web 界面端口访问：`http://homeassistant:9000`（对应 `9099/tcp: 9000`，即 Web UI 端口）。
- 另有 `8000/tcp` 为 Edge Agent API 端口（用于管理远程边缘代理，默认未暴露，需要时开启）。
- 首次访问：默认用户名为 `admin`，默认密码为 `homeassistant`（README 提示实际密码以启动日志为准）。
- 常用操作：查看 Docker 整体概览，管理容器、镜像、网络和数据卷。

## 常见问题
- 如何从备份恢复 Portainer：把备份文件放到挂载进加载项的可访问目录（如 `/share`），在加载项配置中将 `password` 设置为 `empty`，然后重启加载项，即可进入恢复/初始化流程。
- 修改密码会重置数据库：初始化完成后，一旦改动 `password`，加载项会重置 Portainer 数据库，原数据库会被备份到 `/share/portainer_<日期>_<随机数>.backup`，必要时可从加载项配置中恢复。
- 首次使用请先关闭"保护模式"：在加载项主页关闭"保护模式"（Protection mode）后再启动，否则可能无法正常访问 Docker 套接字。

> 注意：该加载项功能强大，几乎可以访问你系统的全部资源，配置不当或缺乏经验的情况下可能损坏系统，请谨慎使用。

---
- 英文原版：Home assistant add-on: Portainer（链接 https://github.com/alexbelgium/hassio-addons/blob/master/portainer/README.md）
- 来源仓库：alexbelgium
