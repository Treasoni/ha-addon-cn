<!-- zh-guide -->
# Postgres 17

## 简介

PostgreSQL（常简称 Postgres）是一款对象关系型数据库管理系统，以可扩展性和对标准的严格遵守著称。作为数据库服务器，它负责安全地存储数据，并按其他应用的请求返回数据，可胜任从单机小应用到拥有大量并发用户的互联网级应用，新版本还提供数据库复制功能用于安全与扩展。本加载项提供 Postgres 17，并支持 VectorChord（pgvector 向量扩展），可直接用于 Immich 等需要向量检索的应用。本加载项基于官方 PostgreSQL 镜像构建。

## 安装

1. 在 Home Assistant → 设置 → 加载项 → 商店，添加本商店仓库：
   - Gitee：https://gitee.com/zhqznc_10603234_123/ha-addon
   - GitHub：https://github.com/Treasoni/ha-addon-cn
2. 搜索 postgres_17 并安装。

## 配置

至少需要设置 `POSTGRES_PASSWORD`。可配置选项如下：

| 配置键 | 类型 / 默认值 | 说明 |
| ------ | ------------- | ---- |
| `POSTGRES_PASSWORD` | 密码，默认 `homeassistant` | postgres 用户的密码，请设置为强密码 |
| `POSTGRES_USER` | 字符串（可选） | 自定义用户名，默认使用 `postgres` |
| `POSTGRES_DB` | 字符串（可选） | 可选的默认数据库名，首次启动时自动创建 |
| `POSTGRES_INITDB_ARGS` | 字符串（可选） | 传给 initdb 的附加参数（如 `--encoding=UTF8 --lc-collate=C --lc-ctype=C`） |
| `POSTGRES_HOST_AUTH_METHOD` | 字符串（可选） | 数据库的主机认证方法（如 `md5`） |
| `env_vars` | 列表（可选） | 附加环境变量列表，每项包含 `name`（变量名）与 `value`（变量值） |

默认端口为 `5432`，默认用户为 `postgres`，密码由 `POSTGRES_PASSWORD` 设置。配置文件 `postgresql.conf` 默认存放在 `/config/postgresql.conf`，可由其他加载项和 Home Assistant 访问，便于用 File Editor 等加载项修改；如需更安全，可将 `CONFIG_LOCATION` 改为 `/data/orig/postgresql.conf` 使其仅本加载项可见。

## 使用 / 访问入口

PostgreSQL 默认端口 `5432/tcp` 映射到宿主端口 `5432`，使用任意 Postgres 客户端连接 `homeassistant.local:5432` 即可访问（默认用户 `postgres`，密码为你设置的 `POSTGRES_PASSWORD`）。

### 从 Postgres 15 迁移

1. 停止 Postgres 15 加载项。
2. 使用 Filebrowser 加载项把数据库目录从 `/addon_configs/xxx-postgres` 复制到 `/addon_configs/xxx-postgres_latest`。
3. 启动 Postgres 17 加载项，数据库升级会自动进行。即使升级失败，你的数据仍安全保留在 Postgres 15 加载项中。

### 安全建议

默认情况下 Postgres 会暴露在宿主机的局域网中。若要只允许 Home Assistant 内的其他加载项访问：

1. 让使用 Postgres 的加载项通过内部 DNS 名称 `db21ed7f-postgres-latest:5432` 连接。
2. 在加载项配置的“网络”部分，清空 `5432` 端口映射。
3. 保存并重启加载项，此后 Postgres 将不再从局域网可达。

## 常见问题

- **连接被拒绝？** 请确认使用的是 `postgres` 用户与你设置的 `POSTGRES_PASSWORD` 密码，并确认宿主机 `5432` 端口未被占用。
- **升级后数据库出问题怎么办？** 本加载项的某些版本包含破坏性变更（例如新增向量扩展、数据目录迁移），升级前请务必先备份数据库，若遇到问题请先恢复备份。
- **Immich 需要向量数据库怎么配置？** 本加载项已内置 VectorChord/pgvector 向量支持，可直接作为 Immich 的 Postgres 数据库使用。
- **数据库文件放在哪里？** 数据目录（PGDATA）位于 `/config/database`，升级后会被保留。
- **如何从 Postgres 15 迁移？** 停止 Postgres 15 后，把数据库目录从 `/addon_configs/xxx-postgres` 复制到 `/addon_configs/xxx-postgres_latest`，再启动本加载项即可自动升级。

---
- 英文原版：Home assistant add-on: Postgres；链接 https://github.com/alexbelgium/hassio-addons/blob/master/postgres_17/README.md
- 来源仓库：alexbelgium
