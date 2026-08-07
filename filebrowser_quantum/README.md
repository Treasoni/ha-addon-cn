<!-- zh-guide -->
# FileBrowser Quantum

## 简介
FileBrowser Quantum 是一款现代、响应式的多源文件管理器，支持实时索引、高级共享以及多种认证方式（密码、免认证、代理、OIDC），用于管理你的 Home Assistant 文件。它是原 FileBrowser 项目的持续维护分支，本加载项基于 gtstef/filebrowser 的 Docker 镜像构建。

## 安装
1. 在 Home Assistant → 设置 → 加载项 → 商店，添加本商店仓库：
   - Gitee：https://gitee.com/zhqznc_10603234_123/ha-addon
   - GitHub：https://github.com/Treasoni/ha-addon-cn
2. 搜索 filebrowser_quantum 并安装。

## 配置
| 配置键 | 类型 / 默认值 | 说明 |
|--------|---------------|------|
| `auth_method` | 枚举（password / noauth / proxy / oidc） / `noauth` | 认证方式：密码 / 免认证 / 代理 / OIDC |
| `default_user_scope` | 字符串 / `/` | FileBrowser 文件源根路径与所有用户的默认作用域，须为已存在的绝对目录（如 `/share`、`/media`） |
| `env_vars` | 列表 / 空 | 额外环境变量（大写或小写命名） |
| `env_vars.name` | 字符串 | 环境变量名，须匹配 `^[A-Za-z0-9_]+$` |
| `env_vars.value` | 字符串（可选） | 环境变量值 |
| `localdisks` | 字符串（可选） / 空 | 要挂载的本地磁盘，例如 `sda1,sdb1,MYNAS` |
| `networkdisks` | 字符串（可选） / 空 | 要挂载的 SMB 远程共享，例如 `//SERVER/SHARE` |
| `cifsusername` | 字符串（可选） / 空 | SMB 共享的用户名 |
| `cifspassword` | 字符串（可选） / 空 | SMB 共享的密码 |
| `cifsdomain` | 字符串（可选） / 空 | SMB 共享的域 |

## 使用 / 访问入口
启动后可在 Home Assistant 侧边栏看到 FileBrowser Quantum 图标，点击进入。

## 常见问题
1. 默认凭据为用户名 `admin`、密码 `admin`。首次登录后请立即在「设置 > 用户管理」中修改默认密码。
2. `auth_method` 默认为 `noauth`（免认证），此时界面无登录保护；如需密码登录，请将其改为 `password`。
3. `default_user_scope` 必须是已存在的绝对目录路径（例如 `/share`、`/media`），用于指定文件源与所有用户的默认作用域。
4. 支持挂载本地磁盘与 SMB 远程共享，具体参见 alexbelgium wiki 中 "Mounting Local Drives in Addons" 与 "Mounting Remote Shares in Addons"。

---
- 英文原版：Home assistant add-on: FileBrowser Quantum；链接 https://github.com/alexbelgium/hassio-addons/blob/master/filebrowser_quantum/README.md
- 来源仓库：alexbelgium
