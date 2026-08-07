<!-- zh-guide -->
# Git pull

## 简介
从 Git 仓库拉取并更新 Home Assistant 的本地配置目录（/config）。本加载项会执行 `git pull`，将你托管在 Git 仓库中的配置同步到本地，并可选地在配置变更且校验通过后自动重启 Home Assistant。

## 安装
1. 在 Home Assistant → 设置 → 加载项 → 商店，添加本商店仓库：
   - Gitee：https://gitee.com/zhqznc_10603234_123/ha-addon
   - GitHub：https://github.com/Treasoni/ha-addon-cn
2. 搜索 git_pull 并安装。

## 配置

| 配置键 | 类型/默认值 | 说明 |
|--------|-------------|------|
| `repository` | 字符串（默认：空） | 你的仓库的 Git 克隆 URL，务必使用双引号包裹。必填。 |
| `git_branch` | 字符串（默认：`master`） | 要更新的分支名；留空则更新当前检出的分支。 |
| `git_remote` | 字符串（默认：`origin`） | 被跟踪的远端名称，不确定时保持 `origin`。 |
| `git_command` | 字符串：`pull` 或 `reset`（默认：`pull`） | 执行的 Git 命令。`pull` 保留本地对已跟踪文件的改动；`reset` 执行 `git reset --hard` 并覆盖本地改动。 |
| `git_prune` | 布尔值（默认：`false`） | 设为 `true` 时清理远程已删除但本地仍有缓存的分支。 |
| `auto_restart` | 布尔值（默认：`false`） | 配置变更且校验通过后是否自动重启 Home Assistant。 |
| `restart_ignore` | 字符串数组（默认：`ui-lovelace.yaml`、`.gitignore`） | 启用 `auto_restart` 后，仅这些文件的变更不会触发 HA 重启；可指定整个目录。 |
| `deployment_user` | 字符串（默认：空） | 使用用户名+密码认证时的用户名。 |
| `deployment_password` | 密码（默认：空） | 认证密码；未设置 `deployment_user` 时忽略。 |
| `deployment_key` | 字符串数组（默认：空） | 用于 Git 操作的私有 SSH 密钥（必须无口令）。SSH 仓库（`<user>@<host>:<repository path>` 格式）必填。 |
| `deployment_key_protocol` | 字符串：`rsa`/`dsa`/`ecdsa`/`ed25519`（默认：`rsa`） | SSH 密钥的协议，通常可由私钥文件名后缀判断，如 `id_rsa` 对应 `rsa`。 |
| `repeat.active` | 布尔值（默认：`false`） | 是否启用定时自动轮询仓库更新。 |
| `repeat.interval` | 整数（默认：`300`） | 自动轮询的间隔，单位秒。 |

## 使用 / 访问入口
- 本加载项没有 Web 界面（无 ingress、不暴露端口），作为后台服务运行，直接读写 Home Assistant 的配置目录 `/config`。
- 首次使用：在“配置”中把 `repository` 填成你的仓库克隆地址，再按需调整其他选项；保存后启动加载项，并打开“日志”查看结果。
- 日志末尾没有错误即表示已成功访问仓库。常见的无错误日志示例：`[Info] Nothing has changed.`、`[Info] Something has changed, checking Home-Assistant config...`、`[Info] Local configuration has changed. Restart required.`
- 如需自动更新：将 `repeat.active` 设为 `true`，并在加载项页面开启“随系统启动”（Start on boot）。

## 常见问题
1. **有整体配置丢失的风险**：首次启动前，请确保你的 Home Assistant 配置在 Git 仓库中有完整备份；否则本地配置目录可能被空配置覆盖，届时需要从备份恢复。
2. **`git reset` 会覆盖本地改动**：`git_command` 选择 `reset` 时，已跟踪文件的本地改动会被覆盖。可用 `git ls-tree -r master --name-only` 查看所有被跟踪的文件。
3. **SSH 密钥必须无口令**：`deployment_key` 填写的私钥不能设置 passphrase，否则 Git 操作认证会失败。

---
- 英文原版：Home Assistant App: Git pull（https://github.com/home-assistant/addons/blob/master/git_pull/README.md）
- 来源仓库：official
