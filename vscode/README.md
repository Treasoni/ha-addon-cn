<!-- zh-guide -->
# Studio Code Server

## 简介

Studio Code Server 是一个基于浏览器访问的 Visual Studio Code（VSCode）加载项，让你可以直接在 Web 浏览器中编辑 Home Assistant 配置，并能嵌入 Home Assistant 前端界面。它基于 `code-server` 以远程服务器方式运行，提供完整的 VSCode 使用体验。

加载项开箱即用地预装并预配置了 Home Assistant、MDI 图标和 YAML 扩展，自动补全开箱即用，无需任何额外配置。

## 安装

1. 在 Home Assistant 中进入「设置 → 加载项 → 商店」，点击右上角菜单添加本商店仓库：
   - Gitee：https://gitee.com/zhqznc_10603234_123/ha-addon
   - GitHub：https://github.com/Treasoni/ha-addon-cn
2. 在商店中搜索 `vscode`（Studio Code Server）并点击安装。
3. 启动加载项并在日志中确认一切正常，然后打开 Web 界面。

## 配置

> 注意：修改配置后需重启加载项才会生效。

| 配置键 | 类型 / 默认值 | 说明 |
| --- | --- | --- |
| `log_level` | 枚举（trace\|debug\|info\|notice\|warning\|error\|fatal），可选 / 空 | 加载项的日志输出级别。`trace` 显示全部细节，`debug` 显示详细调试信息，`info` 为正常事件，`warning` 为非错误的异常，`error` 为无需立即处理的错误，`fatal` 为致命错误。推荐使用 `info`。 |
| `config_path` | 字符串，可选 / 空 | 覆盖加载项打开 Web 界面时的默认路径，例如使用 `/share/myconfig` 替代 `/config`。若设为 `/root`，则 `/config`、`/ssl`、`/share` 等常用目录会作为子文件夹出现。未配置时默认为 `/config`。 |
| `packages` | 字符串列表 / 空 | 需要额外安装到 Shell 环境的 Ubuntu 软件包列表（例如 Python、PHP、Go）。注意：安装较多软件包会明显加长加载项启动时间。 |
| `init_commands` | 字符串列表 / 空 | 自定义 VSCode 环境的初始化命令列表。添加的 shell 命令会在加载项每次启动时执行。 |

## 使用 / 访问入口

启动后可在 Home Assistant 侧边栏看到 Studio Code Server 图标，点击进入即可打开 VSCode 界面编辑配置。

## 常见问题

- **自动补全不生效**：Home Assistant、MDI 图标与 YAML 扩展已预装并预配置，一般无需手动设置；若修改过相关设置，加载项可能不再自动优化这些设置。
- **恢复默认设置**：若想回到加载项提供的默认配置，可在设置中重置 VSCode 设置为加载项默认值。
- **启动较慢**：`packages` 中安装较多软件包会导致启动时间变长，请只安装必要的包。
- **默认打开目录**：未设置 `config_path` 时默认打开 `/config`，可按需指向其他配置目录。

---
- 英文原版：Visual Studio Code；链接 https://github.com/hassio-addons/repository/blob/main/vscode/README.md
- 来源仓库：frenck
