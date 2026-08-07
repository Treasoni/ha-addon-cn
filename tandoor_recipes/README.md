<!-- zh-guide -->
# Tandoor recipes

## 简介

Tandoor recipes 是一个面向个人与家庭的菜谱管理器，适合拥有一批菜谱、希望与亲友分享或整理收藏的用户。它带有基础的权限系统，但设计上不适合作为公开页面对外运行。本加载项基于 TandoorRecipes/recipes 镜像构建。

## 安装

1. 在 Home Assistant → 设置 → 加载项 → 商店，添加本商店仓库：
   - Gitee：https://gitee.com/zhqznc_10603234_123/ha-addon
   - GitHub：https://github.com/Treasoni/ha-addon-cn
2. 搜索 `tandoor_recipes` 并安装。

## 配置

| 配置键 | 类型 / 默认值 | 说明 |
|--------|--------------|------|
| `env_vars` | 列表 / 空 | 额外环境变量列表（每项含 `name` 和 `value`） |
| `ALLOWED_HOSTS` | 字符串 / 默认 `*` | 允许访问的主机名列表（逗号分隔）；通过 Ingress 使用时请填 Home Assistant 地址 |
| `DB_TYPE` | 枚举（sqlite / postgresql_external）/ 默认 `sqlite` | 数据库类型：`sqlite` 或外部 PostgreSQL |
| `DEBUG` | 枚举（0 / 1）/ 默认 `0` | 调试模式（0=正常，1=调试） |
| `SECRET_KEY` | 字符串 / 默认 `YOUR_SECRET_KEY` | Django 安全密钥（必填，请改为随机长字符串） |
| `externalfiles_folder` | 字符串 / 默认 `/config/addons_config/tandoor_recipes/externalfiles` | 外部菜谱文件导入目录 |
| `POSTGRES_DB` | 字符串 / 空 | 外部 PostgreSQL 数据库名（`DB_TYPE` 为 `postgresql_external` 时必填） |
| `POSTGRES_HOST` | 字符串 / 空 | 外部 PostgreSQL 主机 |
| `POSTGRES_PASSWORD` | 字符串（密码）/ 空 | 外部 PostgreSQL 密码 |
| `POSTGRES_PORT` | 字符串 / 空 | 外部 PostgreSQL 端口 |
| `POSTGRES_USER` | 字符串 / 空 | 外部 PostgreSQL 用户名 |
| `AI_API_KEY` | 字符串 / 空 | 访问 LLM 的 API 密钥 |
| `AI_MODEL_NAME` | 字符串 / 空 | 用于 LLM 的模型名称（支持的服务商见 litellm 文档） |
| `AI_RATELIMIT` | 字符串 / 空 | LLM 访问速率限制（使用 DRF 语法） |

## 使用 / 访问入口

Web 界面位于宿主端口 9928。

## 常见问题

- **安全密钥**：`SECRET_KEY` 为必填项，请务必改成一段随机长字符串，不要使用默认值。
- **数据库选择**：默认使用 SQLite；需要外部 PostgreSQL 时，将 `DB_TYPE` 设为 `postgresql_external` 并填写 `POSTGRES_*` 系列选项。
- **外部菜谱导入**：`externalfiles_folder` 目录可用于导入外部菜谱文件，更多说明见 Tandoor 官方文档的 External Recipes 章节。
- **Ingress 支持**：如需通过 Home Assistant Ingress 访问，请参考社区相关帖子并正确配置 `ALLOWED_HOSTS`。

---
- 英文原版：[Tandoor recipes](https://github.com/alexbelgium/hassio-addons/blob/master/tandoor_recipes/README.md)
- 来源仓库：alexbelgium
