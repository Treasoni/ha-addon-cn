<!-- zh-guide -->
# AppDaemon

## 简介

AppDaemon 是一个松散耦合、多线程、沙箱化的 Python 执行环境，用于为 Home Assistant 编写自动化应用，同时提供可配置的仪表盘（HADashboard）。你可以在其中运行 Python 编写的 AppDaemon 应用，并通过示例文件快速上手。本加载项基于 AppDaemon 4.x。

## 安装

1. 在 Home Assistant → 设置 → 加载项 → 商店，添加本商店仓库：
   - Gitee：https://gitee.com/zhqznc_10603234_123/ha-addon
   - GitHub：https://github.com/Treasoni/ha-addon-cn
2. 搜索 appdaemon 并安装。

## 配置

在加载项“配置”页修改配置后，需要重启加载项才能生效。可选配置键如下：

| 配置键 | 类型/默认值 | 说明 |
| ------ | ----------- | ---- |
| `log_level` | 可选 `list(trace|debug|info|notice|warning|error|fatal)`，默认 `info` | 日志输出详细程度：`trace` 输出全部细节；`debug` 输出调试信息；`info` 常规事件；`warning` 非错误的异常事件；`error` 运行时错误；`fatal` 致命错误。更高级别会自动包含更低级别的日志，默认 `info` 是推荐设置，同样影响 AppDaemon 自身的日志级别 |
| `system_packages` | 列表/字符串列表，默认 `空` | 额外安装的 Alpine 系统软件包（如 `g++`、`make`、`ffmpeg`）；添加大量软件包会显著延长启动时间 |
| `python_packages` | 列表/字符串列表，默认 `空` | 额外安装的 Python 软件包（如 `PyMySQL`、`Requests`、`Pillow`）；添加大量软件包会显著延长启动时间 |
| `init_commands` | 列表/字符串列表，默认 `空` | 一条或多条 shell 命令，每次启动加载项时都会执行，用于进一步自定义环境 |

## 使用 / 访问入口

- **HADashboard 仪表盘**：加载项默认将端口 `5050/tcp` 映射到宿主机端口 `5050`，启动后在浏览器地址栏输入你的设备 IP 与端口 `5050` 即可访问仪表盘。
- **配置目录**：本加载项不会替你配置 AppDaemon 或 HADashboard，但首次运行时会创建一些示例文件便于你开始使用；AppDaemon 的配置文件存放在本加载项的配置目录中，详细的配置说明请参考 [AppDaemon 官方文档](http://appdaemon.readthedocs.io/en/latest/)。

## 常见问题

- **为什么 `appdaemon.yaml` 里没有 `token` 和 `ha_url`？** 这是正常的，不是错误。加载项会自动为 AppDaemon 处理与 Home Assistant 的连接 URL 和访问令牌，无需手动填写（与 AppDaemon 官方文档要求不同）。
- **安装了很多软件包，启动很慢？** `system_packages` 和 `python_packages` 中每添加一个包都会在启动时安装，包越多启动时间越长，请按需添加。
- **`init_commands` 什么时候执行？** 每次加载项启动时都会执行列表中的命令，适合做环境初始化工作。
- **如何运行自己的 AppDaemon 应用？** 参考首次运行生成的示例文件，将应用代码放入 AppDaemon 的应用目录并重启加载项。

---
- 英文原版：Home Assistant Community App: AppDaemon；链接 https://github.com/hassio-addons/repository/blob/main/appdaemon/README.md
- 来源仓库：frenck
