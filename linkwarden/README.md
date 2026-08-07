<!-- zh-guide -->
# Linkwarden

## 简介
Linkwarden 是一个协作式书签管理器，用于收集、整理与保存网页和文章，支持团队与个人将书签分类管理，并提供标签、集合与全文搜索等功能。本加载项基于官方 Linkwarden Docker 镜像构建。

## 安装
1. 在 Home Assistant → 设置 → 加载项 → 商店，添加本商店仓库：
   - Gitee：https://gitee.com/zhqznc_10603234_123/ha-addon
   - GitHub：https://github.com/Treasoni/ha-addon-cn
2. 搜索 linkwarden 并安装。

## 配置
`NEXTAUTH_SECRET` 为必填项，首次启动前必须填写。

| 配置键 | 类型 / 默认值 | 说明 |
|--------|--------------|------|
| `NEXTAUTH_SECRET` | 字符串 / 空 | NextAuth.js 认证密钥，必填，建议为至少 32 字符的随机字符串 |
| `NEXTAUTH_URL` | 字符串（可选） | 自定义 NextAuth URL（仅当从外部访问 Linkwarden 时需要） |
| `NEXT_PUBLIC_DISABLE_REGISTRATION` | 布尔（可选） | 是否禁用新用户注册，默认关闭 |
| `NEXT_PUBLIC_CREDENTIALS_ENABLED` | 布尔（可选） | 是否启用用户名/密码登录，默认开启 |
| `STORAGE_FOLDER` | 字符串（可选） | 书签数据文件存放目录，默认 `/config/library` |
| `DATABASE_URL` | 字符串（可选） | 外部 PostgreSQL 数据库连接串，留空则使用内置数据库 |
| `NEXT_PUBLIC_AUTHENTIK_ENABLED` | 布尔（可选） | 是否启用 Authentik SSO 集成，默认关闭 |
| `AUTHENTIK_CUSTOM_NAME` | 字符串（可选） | Authentik 登录按钮的显示名称，默认 `Authentik` |
| `AUTHENTIK_ISSUER` | 字符串（可选） | Authentik OpenID 配置的 Issuer URL |
| `AUTHENTIK_CLIENT_ID` | 字符串（可选） | Authentik 提供商概览中的 Client ID |
| `AUTHENTIK_CLIENT_SECRET` | 字符串（可选） | Authentik 提供商概览中的 Client Secret |
| `NEXT_PUBLIC_OLLAMA_ENDPOINT_URL` | 字符串（可选） | 用于 AI 功能的 Ollama 端点 URL |
| `OLLAMA_MODEL` | 字符串（可选） | 用于 AI 处理的 Ollama 模型名称 |
| `env_vars` | 列表 / 默认 `[]` | 额外传给容器的环境变量（键名需匹配 `^[A-Za-z0-9_]+$`） |

## 使用 / 访问入口
- 通过浏览器访问宿主端口 3000 打开 Web 界面。
- 首次启动后需在界面中创建第一个用户账户。

## 常见问题
- **`NEXTAUTH_SECRET` 怎么填？** 生成一个至少 32 字符的随机字符串并填入；升级到 2.15.1.2 以上版本前建议先做一次完整备份。
- **数据库用哪种？** 默认内置 SQLite；生产环境建议通过 `DATABASE_URL` 连接 PostgreSQL。
- **如何集成 Authentik SSO？** 将 `NEXT_PUBLIC_AUTHENTIK_ENABLED` 设为 `true` 并填写 `AUTHENTIK_*` 相关选项，注意 `AUTHENTIK_ISSUER` 末尾不要带 `/`。

---
- 英文原版：[Home assistant add-on: Linkwarden](https://github.com/alexbelgium/hassio-addons/blob/master/linkwarden/README.md)
- 来源仓库：alexbelgium
