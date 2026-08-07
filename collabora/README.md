<!-- zh-guide -->
# Collabora

## 简介

Collabora Online 是一款基于 LibreOffice 技术的协作式办公套件，提供在线文档编辑能力，常与 Nextcloud 配合使用。

## 安装

1. 在 Home Assistant → 设置 → 加载项 → 商店，添加本商店仓库：
   - Gitee：https://gitee.com/zhqznc_10603234_123/ha-addon
   - GitHub：https://github.com/Treasoni/ha-addon-cn
2. 搜索 `collabora` 并安装。
3. 安装完成后启动 add-on，并查看日志确认启动成功。

## 配置

| 配置键 | 类型 / 默认值 | 说明 |
| --- | --- | --- |
| `env_vars` | 列表 / 空 | 传入容器的额外环境变量（`name`/`value` 形式） |
| `aliasgroup1` | 字符串 / 空 | 允许使用本 Collabora 的 Nextcloud 服务器外部地址（如 `https://nextcloud_domain.com:443`） |
| `aliasgroup2` | 字符串（可选） / 空 | 第二个 Nextcloud 服务器，格式同 `aliasgroup1` |
| `aliasgroup3` | 字符串（可选） / 空 | 第三个 Nextcloud 服务器，格式同 `aliasgroup1` |
| `server_name` | 字符串（可选） / 空 | 本 Collabora 服务器的外部主机名（含端口），即浏览器访问的地址（如 `code.example.com`，需带上端口），反代之后设置 |
| `ssl` | 布尔 / 默认 `false` | 使用 /ssl 中的证书启用 SSL |
| `ssl_termination` | 布尔（可选） / 空 | 当 `ssl` 为 false 但浏览器经反代以 https 访问 Collabora 时设为 true |
| `certfile` | 字符串 / 默认 `fullchain.pem` | /ssl 中的证书文件名 |
| `keyfile` | 字符串 / 默认 `privkey.pem` | /ssl 中的私钥文件名 |
| `cert_domain` | 字符串（可选） / 空 | 当 `ssl` 为 false 时生成自签名证书的通用名 |
| `username` | 字符串 / 空 | Collabora 管理员控制台用户名 |
| `password` | 密码 / 空 | Collabora 管理员控制台密码 |
| `extra_params` | 字符串（可选） / 空 | 传递给 Collabora 启动脚本的额外参数 |
| `dictionaries` | 字符串（可选） / 空 | 需要安装的词典语言列表（空格分隔） |
| `domain1` | 字符串（可选） / 空 | 已废弃，请使用 `server_name` |

## 使用 / 访问入口

Web 界面（管理员控制台）可通过 `https://<宿主地址>:9980/browser/dist/admin/admin.html` 访问（端口 9980）。

## 常见问题

- `aliasgroup1/2/3` 会被 Collabora 作为正则表达式匹配，点号需使用单个反斜杠转义（如 `next\.duckdns\.org`），双反斜杠不会匹配真实主机名。
- `server_name` 不是正则表达式，直接写纯主机名（不带反斜杠）。
- 与 Nextcloud 配合时：`aliasgroup1` 是 Nextcloud 的地址，`server_name` 是 Collabora 的地址。两者填反是「无法连接 Collabora Online 服务器」最常见的原因。
- 若 add-on 使用自签名证书，在 Nextcloud 的 Nextcloud Office 设置中可勾选「禁用证书验证」。

---
- 英文原版：[Home assistant add-on: Collabora](https://github.com/alexbelgium/hassio-addons/blob/master/collabora/README.md)
- 来源仓库：alexbelgium
