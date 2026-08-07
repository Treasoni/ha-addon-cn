<!-- zh-guide -->
# Immich

## 简介
Immich 是一款可直接从手机备份照片和视频的自托管解决方案，本加载项基于 imagegenius 的 [docker-immich](https://github.com/imagegenius/docker-immich) 镜像打包，跟踪 **Immich v3** 主线（`ghcr.io/imagegenius/immich:3` 镜像系列）。

> ⚠️ 上游项目仍处于积极开发中，可能存在 Bug 和变动，开发者也提醒：不要把它当作照片和视频的唯一存储方式。

## 安装
1. 在 Home Assistant → 设置 → 加载项 → 商店，添加本商店仓库：
   - Gitee：https://gitee.com/zhqznc_10603234_123/ha-addon
   - GitHub：https://github.com/Treasoni/ha-addon-cn
2. 搜索 **immich** 并安装。
3. 配置数据库等选项后点击「保存」，然后启动加载项并查看日志确认一切正常。

**注意**：Immich 依赖独立的 PostgreSQL 数据库，请从本商店一并安装并配置 Postgres 加载项（推荐搭配见「常见问题」）。务必在**启动之前**改好数据库密码，启动后不会再变更。

## 配置
各选项（来自 config.yaml 的 schema，类型/默认值取自 config.yaml 与 README）：

| 配置键 | 类型 / 默认值 | 说明 |
|--------|--------------|------|
| `data_location` | str / `/share/immich` | Immich 数据存放路径 |
| `library_location` | str（可选） | 照片/视频库路径，可指向数据目录之外的挂载盘；会自动软链到 `data_location/library`（不会移动已有文件，需自行处理） |
| `TZ` | str（可选）/ `Europe/Paris` | 时区，例如 `Europe/London` |
| `localdisks` | str（可选） | 要挂载的本地磁盘，例如 `sda1,sdb1,MYNAS` |
| `networkdisks` | str（可选） | 要挂载的 SMB 共享，例如 `//SERVER/SHARE` |
| `cifsusername` | str（可选） | SMB 用户名 |
| `cifspassword` | str（可选） | SMB 密码 |
| `cifsdomain` | str（可选） | SMB 域 |
| `DB_HOSTNAME` | str / `homeassistant.local` | 数据库主机名；设为 `homeassistant.local` 时会自动改写为宿主机检测到的 IP |
| `DB_USERNAME` | str / `postgres` | 数据库用户名 |
| `DB_PASSWORD` | str | 数据库密码（必填，启动前改好） |
| `DB_DATABASE_NAME` | str / `immich` | 数据库名 |
| `DB_PORT` | int / `5432` | 数据库端口 |
| `DB_ROOT_PASSWORD` | str（可选） | 数据库 root 密码；未设置时启动会自动生成并写入选项 |
| `JWT_SECRET` | str | JWT 认证密钥（必填） |
| `DISABLE_MACHINE_LEARNING` | bool / `false` | 设为 `true` 禁用机器学习（AI 相关）功能 |
| `MACHINE_LEARNING_WORKERS` | int（可选）/ `1` | 机器学习 worker 数量 |
| `MACHINE_LEARNING_WORKER_TIMEOUT` | int（可选）/ `120` | 机器学习 worker 超时（秒） |
| `VIPS_NOVECTOR` | bool / `false` | 设为 `true` 导出 `VIPS_NOVECTOR=1`，用于绕开 aarch64 上缩略图生成异常 |
| `skip_permissions_check` | bool / `false` | 跳过文件权限检查（每次启动权限修正耗时过长时可开启） |
| `env_vars` | 数组（可选） | 追加自定义环境变量（键名需匹配 `^[A-Za-z0-9_]+$`，值为字符串） |

**配置示例**：

```yaml
data_location: "/share/immich"
library_location: "/media/photos"
TZ: "Asia/Shanghai"
localdisks: "sda1,sdb1"
networkdisks: "//192.168.1.100/photos"
cifsusername: "photouser"
cifspassword: "password123"
DB_HOSTNAME: "homeassistant.local"
DB_USERNAME: "postgres"
DB_PASSWORD: "secure_password"
DB_DATABASE_NAME: "immich"
JWT_SECRET: "your-secret-key-here"
```

**把数据存到挂载的本地磁盘**：将 `localdisks` 设为你硬盘的名称（如 `sda1`），磁盘会挂载到 `/mnt/sda1`；再把 `data_location` 指向挂载路径，例如 `/mnt/sda1/immich`。

## 使用 / 访问入口
- **Web UI 端口**：`8080`（config.yaml 中 `8080/tcp` 默认映射到宿主机 **8181** 端口）。可在浏览器通过 `http://<你的IP>:8181` 访问（上游 README 的描述为 `<your-ip>:8080`）；本加载项未启用 ingress，直接访问端口即可。
- **首次访问**：先配置好 PostgreSQL 数据库连接（`DB_HOSTNAME` / `DB_USERNAME` / `DB_PASSWORD` 等），启动时脚本会自动创建数据库与用户。数据库不可达时加载项会停止并提示。
- 启动后即可在 Web 界面中浏览、上传并管理照片和视频，并通过手机端备份照片与视频。

## 常见问题
1. **需要哪种数据库？** Immich v3 要求 PostgreSQL 14–17 且带有 **VectorChord（`vchord`）** 扩展，上游已移除对 `pgvecto.rs` 的支持。本仓库的 `Postgres 15` / `Postgres 17` 加载项已提供该能力，是推荐搭配；也可使用官方 `ghcr.io/immich-app/postgres:*-vectorchord*` 镜像。Immich 首次启动时会自行创建并校验该扩展。
2. **从 Immich v2 升级到 v3 要注意什么？** 保留现有支持 VectorChord 的数据库，让 Immich 自动迁移数据；若数据库仍存放旧 `pgvecto.rs` 扩展的数据，请等 Immich 完成迁移后再移除该扩展。详见官方迁移指南：https://immich.app/blog/v3-migration
3. **对硬件有要求吗？** 在 `amd64` 架构上，Immich v3 需要 x86-64-v2（或更新）的 CPU。

---
- 英文原版：Home assistant add-on: immich（https://github.com/alexbelgium/hassio-addons/blob/master/immich/README.md）
- 来源仓库：alexbelgium
