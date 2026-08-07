<!-- zh-guide -->
# Spotweb

## 简介

Spotweb 是一个基于 Spotnet 协议的去中心化 Usenet 社区客户端，是当前功能最丰富的 Spotnet 客户端之一。它提供快速检索、内置自定义过滤器、上次浏览后的新帖标记、收藏列表，并可作为 `newznab` 提供方与 SickGear、Sick Beard、CouchPotato 集成，也支持 Sabnzbd 与 nzbget 集成、多语言与多用户。本加载项基于 spotweb/spotweb 镜像构建。

## 安装

1. 在 Home Assistant → 设置 → 加载项 → 商店，添加本商店仓库：
   - Gitee：https://gitee.com/zhqznc_10603234_123/ha-addon
   - GitHub：https://github.com/Treasoni/ha-addon-cn
2. 搜索 `spotweb` 并安装。

## 配置

> 注意：本加载项需要 MySQL 数据库。请确保已安装 MariaDB 加载项，或使用远程 MySQL 服务器。检测到 MariaDB 加载项时会自动创建数据库和用户。

| 配置键 | 类型 / 默认值 | 说明 |
|--------|--------------|------|
| `certfile` | 字符串 / 默认 `fullchain.pem` | SSL 证书文件名 |
| `keyfile` | 字符串 / 默认 `privkey.pem` | SSL 私钥文件名 |
| `ssl` | 布尔 / 默认 `false` | 是否启用 SSL |
| `env_vars` | 列表 / 空 | 额外环境变量列表（每项含 `name` 和 `value`） |
| `log_level` | 枚举（trace / debug / info / notice / warning / error / fatal）/ 空 | 日志级别 |
| `remote_mysql_database` | 字符串 / 空 | 远程 MySQL 数据库名 |
| `remote_mysql_host` | 字符串 / 空 | 远程 MySQL 主机 |
| `remote_mysql_password` | 字符串（密码）/ 空 | 远程 MySQL 密码 |
| `remote_mysql_port` | 整数 / 空 | 远程 MySQL 端口 |
| `remote_mysql_username` | 字符串 / 空 | 远程 MySQL 用户名 |

## 使用 / 访问入口

Spotweb 支持 Ingress，启动后可在 Home Assistant 侧边栏看到 Spotweb 图标，点击进入。若需通过端口访问，宿主端口为 9999。

## 常见问题

- **数据库依赖**：需要 MySQL/MariaDB。检测到 MariaDB 加载项时会自动创建数据库与用户；使用远程 MySQL 时，请填写 `remote_mysql_*` 系列选项。
- **安全认证**：得益于 Ingress 支持，安全与认证由 Home Assistant 处理，因此 Spotweb 自身的认证默认关闭，安装后通过 Ingress 界面即可直接使用。
- **首次同步**：后台任务每小时拉取一次帖子。输入凭据后重启加载项即可触发首次同步。
- **自定义配置**：如需导入自己的 `ownsettings.php`，请把文件放到 `/config/addons_config/spotweb/ownsettings.php`。

---
- 英文原版：[Spotweb](https://github.com/alexbelgium/hassio-addons/blob/master/spotweb/README.md)
- 来源仓库：alexbelgium
