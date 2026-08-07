<!-- zh-guide -->
# Bookstack

## 简介

Bookstack 是一款简单、免费的开源 Wiki 软件，适合用于记录文档、搭建团队知识库或个人笔记。它提供直观的界面来组织书籍、章节与页面，并支持基于角色的访问控制。本加载项将 Bookstack 打包为 Home Assistant 加载项，可直接通过浏览器使用。

## 安装

1. 在 Home Assistant → 设置 → 加载项 → 商店，添加本商店仓库：
   - Gitee：https://gitee.com/zhqznc_10603234_123/ha-addon
   - GitHub：https://github.com/Treasoni/ha-addon-cn
2. 搜索 bookstack 并安装。

## 配置

在加载项“配置”页修改配置后，需要重启加载项才能生效。可选配置键如下：

| 配置键 | 类型/默认值 | 说明 |
| ------ | ----------- | ---- |
| `log_level` | 可选 `list(trace|debug|info|notice|warning|error|fatal)`，默认 `info` | 日志输出详细程度：`trace` 输出全部细节；`debug` 输出调试信息；`info` 常规事件；`warning` 非错误的异常事件；`error` 运行时错误；`fatal` 致命错误。更高级别会自动包含更低级别的日志，默认 `info` 是推荐设置 |
| `ssl` | `bool`，默认 `false` | 是否在 Bookstack Web 界面启用 SSL（HTTPS），设为 `true` 启用 |
| `certfile` | `str`，默认 `fullchain.pem` | 用于 SSL 的证书文件，必须存放在 `/ssl/` 目录 |
| `keyfile` | `str`，默认 `privkey.pem` | 用于 SSL 的私钥文件，必须存放在 `/ssl/` 目录 |
| `remote_mysql_host` | 可选 `str`，默认 `空` | 使用外部数据库时，MySQL/MariaDB 数据库的主机名或地址 |
| `remote_mysql_database` | 可选 `str`，默认 `空` | 仅使用外部数据库时生效，数据库名称 |
| `remote_mysql_username` | 可选 `str`，默认 `空` | 仅使用外部数据库时生效，有权限的数据库用户名 |
| `remote_mysql_password` | 可选 `str`（密码），默认 `空` | 仅使用外部数据库时生效，上述用户的密码 |
| `remote_mysql_port` | 可选 `int`，默认 `空` | 仅使用外部数据库时生效，数据库服务器监听的端口 |
| `show_appkey` | 可选 `bool`，默认 `空` | 设为 `true` 时会在加载项日志中显示当前配置的 appkey，建议在恢复前记录 |
| `appkey` | 可选 `str`，默认 `空` | 从其他系统恢复时由用户自定义 appkey；若已设置，会在首次运行时自动从配置中移除 |
| `envvars` | 列表/对象列表（含 `name`、`value` 子键），默认 `空` | 设置环境变量以控制 Bookstack 的配置（详见 Bookstack 官方文档）；选项区分大小写，且由具体配置设置的项优先。修改这些选项可能引发问题，风险自负 |

## 使用 / 访问入口

- **Web 界面**：加载项默认将端口 `80/tcp` 映射到宿主机端口 2665。启动后在浏览器地址栏输入你的设备 IP 与端口 2665 即可访问 Bookstack Web 界面；若启用了 `ssl`，请改用 HTTPS 协议访问。
- **数据库**：默认情况下，Bookstack 会自动使用并配置 Home Assistant 的 MariaDB 加载项（需提前安装），也可在配置中改用外部的 MySQL/MariaDB 数据库。

## 常见问题

- **Ingress 不可用？** 由于应用存储图片文件的方式所限，本加载项不支持 Ingress 访问，请直接通过端口 2665 访问 Web 界面。
- **首次启动失败？** Bookstack 默认依赖 Home Assistant 的 MariaDB 加载项，请确保先安装并启动 MariaDB 加载项。
- **如何在外部数据库和内置数据库之间切换？** 默认使用内置 MariaDB；若要改用外部 MySQL/MariaDB，请填写 `remote_mysql_*` 相关配置。注意两者之间没有简单的升级路径，切换前请备份数据。
- **如何更换应用密钥（appkey）？** 从其他系统恢复时，可设置 `appkey` 来复用原有密钥，并可将 `show_appkey` 设为 `true` 在日志中查看当前 appkey 以便记录。

---
- 英文原版：Home Assistant Community Add-on: Bookstack；链接 https://github.com/hassio-addons/repository/blob/main/bookstack/README.md
- 来源仓库：frenck
