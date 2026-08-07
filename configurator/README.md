<!-- zh-guide -->
# File editor（文件编辑器）

## 简介
File editor（原名 Configurator）是一款基于浏览器的文件编辑器，用于直接修改 Home Assistant 运行主机上的配置文件。它由 Ace 编辑器驱动，支持多种代码/标记语言的语法高亮，并在编辑时自动检查 YAML 文件的语法错误（Home Assistant 配置默认使用 YAML）。

## 安装
1. 在 Home Assistant → 设置 → 加载项 → 商店，添加本商店仓库：
   - Gitee：https://gitee.com/zhqznc_10603234_123/homeassistant
   - GitHub：https://github.com/Treasoni/ha-addon-cn
2. 搜索 configurator 并安装。

## 配置
该加载项通常无需额外配置即可使用。以下为可选配置项：

| 配置键 | 类型 / 默认值 | 说明 |
|--------|--------------|------|
| `dirsfirst` | bool / `false` | 在文件浏览器树中让目录显示在文件之前。设为 `true` 时目录排在前，`false` 时按默认顺序。 |
| `enforce_basepath` | bool / `true` | 设为 `true` 时，仅允许访问 `/homeassistant` 目录（即 Home Assistant 内的 `/config` 目录）中的文件。 |
| `git` | bool / `true` | 设为 `true` 时，对支持 git 的目录初始化 git 仓库（默认开启，可关闭）。 |
| `ignore_pattern` | 字符串数组 / `["__pycache__", ".cloud", ".storage", "deps"]` | 在文件浏览器树中隐藏匹配这些模式的文件和文件夹。 |
| `ssh_keys` | 字符串数组 / `[]` | SSH 私钥文件名的列表，用于允许访问远程 git 仓库。 |

## 使用 / 访问入口
- 该加载项仅能通过 Ingress 访问，没有独立的直接端口访问，请在 Home Assistant 界面中打开。
- 安装后在 Home Assistant 侧边栏中启用“显示在侧边栏”并在浏览器中刷新，即可从侧边栏进入 File editor。
- 常用功能：
  - 带语法高亮和 YAML 语法检查的在线编辑。
  - 上传和下载文件。
  - 在 git 仓库中暂存（stage）、贮藏（stash）和提交更改，创建与切换分支、推送到远程、查看差异。
  - 列出可用的实体、触发器、事件、条件和服务。
  - 一键重启 Home Assistant，并可重新加载 group、自动化等（需要 API 密码）。
  - 提供 Home Assistant 文档和图标链接。
  - 可在应用容器内执行 Shell 命令。
  - 编辑器设置保存在浏览器中。

## 常见问题
- 只能通过 Ingress 访问：该加载项只能经由 Home Assistant 界面（Ingress）使用，没有直接端口访问。
- YAML 语法错误：编辑 Home Assistant 配置时，YAML 会自动进行语法检查，出现错误时会有提示。
- SSH 私钥：若要访问远程 git 仓库，请在 `ssh_keys` 中填写私钥文件的文件名；加载项启动时会将这些密钥加入 SSH agent。

---
- 英文原版：Home Assistant App: File editor（链接 https://github.com/home-assistant/addons/blob/master/configurator/README.md）
- 来源仓库：official
