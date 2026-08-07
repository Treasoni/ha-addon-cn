<!-- zh-guide -->
# JupyterLab

## 简介

JupyterLab 是一款开源的 Web 应用，让你可以创建并分享包含实时代码、公式、可视化图表与说明文字在内的文档，可用于数据清洗与转换、数值模拟、统计建模、数据可视化、机器学习等众多场景。本加载项运行 JupyterLab——Project Jupyter 的下一代用户界面，一个基于 Jupyter Notebook 与架构、支持交互式与可复现计算的可扩展环境。

## 安装

1. 在 Home Assistant → 设置 → 加载项 → 商店，添加本商店仓库：
   - Gitee：https://gitee.com/zhqznc_10603234_123/ha-addon
   - GitHub：https://github.com/Treasoni/ha-addon-cn
2. 搜索 jupyterlab 并安装。

## 配置

在加载项“配置”页修改配置后，需要重启加载项才能生效。可选配置键如下：

| 配置键 | 类型/默认值 | 说明 |
| ------ | ----------- | ---- |
| `log_level` | 可选 `list(trace|debug|info|notice|warning|error|fatal)`，默认 `info` | 日志输出详细程度：`trace` 输出全部细节；`debug` 输出调试信息；`info` 常规事件；`warning` 非错误的异常事件；`error` 运行时错误；`fatal` 致命错误。更高级别会自动包含更低级别的日志，默认 `info` 是推荐设置 |
| `github_access_token` | `str`（密码），默认 `空` | GitHub 访问令牌。未认证时 GitHub 对仓库数据的请求有较严格的速率限制，可能很快触顶；配置此令牌可显著提升请求额度。支持 secrets 写法，如 `!secret github_token` |
| `system_packages` | 列表/字符串列表，默认 `空` | 额外安装到 JupyterLab 环境中的 Debian 软件包（如 `g++`、`make`、`ffmpeg`）；添加大量软件包会延长启动时间 |
| `init_commands` | 列表/字符串列表，默认 `空` | 一条或多条 shell 命令，每次加载项启动时都会执行，用于进一步自定义环境（如 `pip install`） |

## 使用 / 访问入口

- **Web 界面**：加载项支持 Ingress，启动后可在 Home Assistant 侧边栏看到 JupyterLab 图标，点击进入。加载项已接入 Home Assistant API，可直接在 Notebook 中访问 Home Assistant 的数据。

## 常见问题

- **经常遇到 GitHub API 速率限制？** 未配置令牌时，对 GitHub 仓库数据的未认证请求会在几分钟内触顶。请按文档步骤生成一个带 `repo` 权限的 GitHub Personal Access Token，并填入 `github_access_token`（也可用 `!secret github_token` 引用密钥）。
- **`init_commands` 什么时候执行？** 每次加载项启动时都会执行列表中的命令，适合做环境初始化工作。
- **安装了很多软件包，启动很慢？** `system_packages` 中每添加一个 Debian 包都会在启动时安装，包越多启动时间越长，请按需添加。
- **令牌泄露了怎么办？** GitHub 访问令牌相当于你的 GitHub 账号密码，请不要公开分享或提交到版本库，一旦泄露请立即在 GitHub 中吊销并重新生成。

---
- 英文原版：Home Assistant Community Add-on: JupyterLab；链接 https://github.com/hassio-addons/repository/blob/main/jupyterlab/README.md
- 来源仓库：frenck
