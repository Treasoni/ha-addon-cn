<!-- zh-guide -->
# Ente

## 简介
Ente 是一个自托管、端到端加密的照片与视频存储方案。本加载项提供完整的 Ente 服务器，包括 museum API 服务器与 MinIO S3 兼容存储后端，支持端到端加密备份、人脸识别与搜索、跨平台 App、手机相册自动备份、与家人好友分享相册等功能。本项目基于官方 Ente 服务器构建。

## 安装
1. 在 Home Assistant → 设置 → 加载项 → 商店，添加本商店仓库：
   - Gitee：https://gitee.com/zhqznc_10603234_123/ha-addon
   - GitHub：https://github.com/Treasoni/ha-addon-cn
2. 搜索 ente 并安装。

## 配置
加载项内置 PostgreSQL（元数据）与 MinIO S3（照片/视频内容），MinIO 凭据已硬编码在内部，仅需关注以下选项：

| 配置键 | 类型 / 默认值 | 说明 |
|--------|---------------|------|
| `ENTE_ENDPOINT_URL` | 字符串 / `http://homeassistant.local:8280` | Ente API 的对外访问地址（Web 界面使用） |
| `DB_PASSWORD` | 字符串 / `ente` | 内置 PostgreSQL 的数据库密码 |
| `USE_EXTERNAL_DB` | 布尔 / `false` | 是否使用外部 PostgreSQL 数据库 |
| `TZ` | 字符串（可选） / `Europe/Paris` | 时区设置 |
| `env_vars` | 列表 / 空 | 额外环境变量（大写或小写命名） |
| `env_vars.name` | 字符串 | 环境变量名，须匹配 `^[A-Za-z0-9_]+$` |
| `env_vars.value` | 字符串（可选） | 环境变量值 |

如需使用外部 PostgreSQL（`USE_EXTERNAL_DB: true`），再配置以下键：

| 配置键 | 类型 / 默认值 | 说明 |
|--------|---------------|------|
| `DB_HOSTNAME` | 字符串（可选） / 空 | 外部 PostgreSQL 主机名 |
| `DB_PORT` | 整数（可选） / 空 | 外部 PostgreSQL 端口，留空时默认 `5432` |
| `DB_USERNAME` | 字符串（可选） / 空 | 外部 PostgreSQL 用户名 |
| `DB_DATABASE_NAME` | 字符串（可选） / 空 | 外部 PostgreSQL 数据库名 |

本加载项还支持挂载本地磁盘与 SMB 远程共享，可设置 `localdisks`、`networkdisks`、`cifsusername`、`cifspassword`、`cifsdomain`（均为可选字符串）。

## 使用 / 访问入口
本加载项未启用 Ingress，通过端口访问：
- **Web 界面**：容器端口 `3000/tcp` 映射到宿主端口 `8300`（http://homeassistant:8300）
- **API（museum，App 接入主入口）**：容器端口 `8080/tcp` 映射到宿主端口 `8280`
- 其余服务端口 `3001/tcp` 至 `3009/tcp` 分别映射到宿主 `8301` 至 `8309`（Accounts、Albums、Auth、Cast、Share、Embed、Paste、Locker、Memories），可按需使用。
- MinIO S3 仅内部监听（127.0.0.1），由 museum 代理全部 S3 操作，不对外部开放。

首次使用：下载 Ente 手机 App，在设置中选择「自定义服务器」并填写你的加载项地址（`http://<homeassistant-ip>:8280`），然后在 App 中创建账号。

## 常见问题
1. 自托管实例的订阅验证码无法通过邮件发送，请查看加载项日志中的 `Verification code: xxxxxx` 来完成账号验证。
2. 照片与视频默认存储在 `/config/minio-data`，可挂载更大容量的外部存储。建议定期备份 `/config/minio-data` 与加载项配置。
3. Web 界面始终启用；若遇到 Web UI 500 错误，更新到较新版本（已修复 nginx 重写循环问题）。
4. 使用外部数据库时，`DB_PORT` 留空会自动使用默认端口 `5432`。

---
- 英文原版：Home assistant add-on: Ente；链接 https://github.com/alexbelgium/hassio-addons/blob/master/ente/README.md
- 来源仓库：alexbelgium
