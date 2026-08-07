<!-- zh-guide -->
# Manyfold

## 简介
Manyfold 是一个开源的 3D 模型管理器。本加载项将 Manyfold 打包为 Home Assistant 加载项，数据（应用数据、数据库、缓存、设置）持久化在 `/config`（addon_config）下，并通过可配置的库路径使用宿主机存储；无需外部 PostgreSQL 或 Redis，支持 `amd64` 与 `aarch64` 架构。

## 安装
1. 在 Home Assistant → 设置 → 加载项 → 商店，添加本商店仓库：
   - Gitee：https://gitee.com/zhqznc_10603234_123/ha-addon
   - GitHub：https://github.com/Treasoni/ha-addon-cn
2. 搜索 manyfold 并安装。
3. 首次启动前，请确保宿主机上的库目录已存在（默认 `/share/manyfold/models`）。

## 配置

| 配置键 | 类型 / 默认值 | 说明 |
|--------|--------------|------|
| `secret_key_base` | 字符串 / 空 | Rails 应用密钥，用于签名/加密会话与令牌；留空则首次启动自动生成并持久化，建议保持留空不要修改 |
| `public_hostname` | 字符串（可选） | 生成链接所用的主机名或服务器 IP；留空时自动检测 Home Assistant 外部 URL，回退到 `homeassistant.local` |
| `puid` | 整数 / 默认 `1000` | 应用到可写映射目录（/config 路径）的所有权 UID |
| `pgid` | 整数 / 默认 `1000` | 应用到可写映射目录的所有权 GID |
| `multiuser` | 布尔 / 默认 `true` | 是否启用 Manyfold 多用户模式 |
| `library_path` | 字符串 / 默认 `/share/manyfold/models` | 扫描/索引的库路径 |
| `thumbnails_path` | 字符串 / 默认 `/config/thumbnails` | 缩略图与索引产物持久化路径（必须位于 /config 下） |
| `log_level` | 枚举 / 默认 `info` | 日志级别：`info`、`debug`、`warn`、`error` |
| `web_concurrency` | 整数 / 默认 `4` | Puma worker 进程数 |
| `rails_max_threads` | 整数 / 默认 `16` | 每个 Puma worker 的最大线程数 |
| `default_worker_concurrency` | 整数 / 默认 `4` | Sidekiq 默认队列并发数 |
| `performance_worker_concurrency` | 整数 / 默认 `1` | Sidekiq 性能队列并发数 |
| `max_file_upload_size` | 整数 / 默认 `1073741824` | 最大上传归档大小（字节） |
| `max_file_extract_size` | 整数 / 默认 `1073741824` | 最大解压归档大小（字节） |

## 使用 / 访问入口
- 通过浏览器访问宿主端口 3214 打开 Manyfold Web 界面。
- 将 STL/3MF 等模型文件放入宿主机的 `/share/manyfold/models`，在 Manyfold 界面中配置指向同一容器路径的库，即可开始索引。

## 常见问题
- **提示以 root 运行（安全风险）？** 在加载项配置中把 `puid`/`pgid` 设为非 root 的 UID/GID（如 1000），保存并重启加载项。
- **`secret_key_base` 能改吗？** 首次安装留空会自动生成并保存到 `/config/secret_key_base`；一旦手动设置过再清空，会重新生成密钥并导致所有会话登出。
- **启动失败？** 若 `library_path` 或 `thumbnails_path` 解析到映射存储根目录之外会拒绝启动；`thumbnails_path` 必须位于 `/config` 下以确保持久化。

---
- 英文原版：[Manyfold Home Assistant Add-on](https://github.com/alexbelgium/hassio-addons/blob/master/manyfold/README.md)
- 来源仓库：alexbelgium
