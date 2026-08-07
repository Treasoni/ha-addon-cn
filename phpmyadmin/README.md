<!-- zh-guide -->
# phpMyAdmin

## 简介

phpMyAdmin 是 MySQL 与 MariaDB 的数据库管理工具，专为管理官方 Home Assistant MariaDB 加载项而设计。通过 Web 界面即可完成大多数常用操作——管理数据库、数据表、列、关系、索引、用户和权限等，同时仍可直接执行任意 SQL 语句。

## 安装

1. 在 Home Assistant 中进入「设置 → 加载项 → 商店」，点击右上角菜单添加本商店仓库：
   - Gitee：https://gitee.com/zhqznc_10603234_123/ha-addon
   - GitHub：https://github.com/Treasoni/ha-addon-cn
2. 在商店中搜索 `phpmyadmin`（phpMyAdmin）并点击安装。
3. 安装并启动加载项即可使用。

## 配置

> 注意：修改配置后需重启加载项才会生效。

| 配置键 | 类型 / 默认值 | 说明 |
| --- | --- | --- |
| `log_level` | 枚举（trace\|debug\|info\|notice\|warning\|error\|fatal），可选 / 空 | 加载项的日志输出级别。`trace` 显示全部细节，`debug` 显示详细调试信息，`info` 为正常事件，`warning` 为非错误的异常，`error` 为无需立即处理的错误，`fatal` 为致命错误。推荐使用 `info`。 |
| `upload_limit` | 整数，可选 / 空 | 上传大小限制，用于导入等操作。默认限制为 64MB，可通过此选项调大，例如设为 `100` 表示 100MB。 |

## 使用 / 访问入口

启动后可在 Home Assistant 侧边栏看到 phpMyAdmin 图标，点击进入即可打开管理界面。

## 常见问题

- **需要 MariaDB 加载项**：本加载项需要官方 MariaDB 加载项（2.0 及以上版本）才能运行。
- **仅支持官方 MariaDB**：本加载项专为管理 Home Assistant 官方 MariaDB 加载项设计，无法连接其他 MySQL 或 MariaDB 服务器。
- **导入大文件受限**：默认上传限制为 64MB，如需导入更大的文件，可在配置中调高 `upload_limit`。
- **适用的架构**：本加载项支持 aarch64、amd64，已停止对 armv7 的支持。

---
- 英文原版：phpMyAdmin；链接 https://github.com/hassio-addons/repository/blob/main/phpmyadmin/README.md
- 来源仓库：frenck
