<!-- zh-guide -->
# HACS 极速版国内安装器

这是一个面向 Home Assistant OS `amd64` / `aarch64` 的一次性安装器。它从 Gitee 固定 commit 下载 HACS China 第三方 fork，从清华 TUNA 下载并校验前端和 `aiogithubapi` 依赖，然后把文件写入 Home Assistant 配置目录。

## 简介

适合以下情况：`get.hacs.vip`、GitHub 或默认 PyPI 在当前网络不可达，但 Gitee 和清华 TUNA 可用。

安装关键路径只访问：

- Gitee：HACS China 固定源码 commit；
- 清华 TUNA：固定前端 wheel 和 `aiogithubapi` wheel。

HACS China 是第三方 fork，不是官方 HACS。安装完成后，HACS 运行时访问仓库仍依赖 fork 自带代理；公益代理可能失效，不承诺永久稳定。

## 安装

建议先使用 `haos-mirror-switcher` 完成 Supervisor 镜像源检查，再安装本加载项。两者保持独立，本安装器本身使用国内预构建镜像入口。

1. 在 Home Assistant → 设置 → 加载项 → 商店 → 右上角菜单，添加商店仓库：
   - Gitee：<https://gitee.com/zhqznc_10603234_123/ha-addon>
   - GitHub：<https://github.com/Treasoni/ha-addon-cn>
2. 搜索“HACS 极速版国内安装器”，安装并启动。
3. 等待日志显示安装完成，然后**手动重启 Home Assistant**。
4. 重启后到 设置 → 设备与服务 → 添加集成，搜索并添加 HACS。

本加载项不自动重启 Home Assistant，避免小白用户在不知情时中断服务。

## 配置

这是一次性安装器，默认不会覆盖已有 HACS。

| 配置键 | 类型 / 默认值 | 说明 |
|---|---|---|
| `replace_existing` | `bool` / `false` | 检测到已有 `custom_components/hacs` 时是否允许覆盖；默认拒绝并且不修改任何文件 |

固定安装版本如下，不需要用户填写：

| 组件 | 固定值 | 说明 |
|---|---|---|
| HACS China tag | `2.0.5.3` | 用于 manifest 显示版本 |
| HACS China commit | `d1c828dd078736ec663951844786cf8285e18b4d` | 源码下载按 commit 固定，不追踪最新分支或 tag |
| 前端 | `20250128065759` | 从 TUNA 下载并校验 SHA-256 |
| `aiogithubapi` | `24.6.0` | 从 TUNA 下载、校验并预置到 `/config/deps` |

## 使用 / 访问入口

普通用户只需要：确认配置 → 启动一次 → 看日志 → 手动重启 Home Assistant。

- **已有 HACS 且 `replace_existing: false`**：日志返回 `EXISTING_HACS_REQUIRES_CONFIRMATION`，不会下载、备份或修改已有目录。
- **确认覆盖**：把 `replace_existing` 改为 `true` 后重新启动。覆盖前会把旧目录备份到 `/config/hacs-cn-backups/`，最近保留三份；安装或校验失败会尝试恢复旧目录和依赖。
- **依赖预置**：`aiogithubapi` 会自动写入 `/config/deps`，保留该目录中的其他依赖，不要求进入 Home Assistant 容器手工执行 pip。
- **安装后复验**：程序会检查 HACS manifest、前端版本和 `aiogithubapi` 可导入性；任何一项失败都会返回明确错误码并停止。

典型成功日志最后会提示：重启 Home Assistant，然后在“设置 → 设备与服务 → 添加集成”中搜索 HACS。

## 常见问题

- **为什么不能直接覆盖已有 HACS？** 默认安全策略是先停下来让你确认。只有把 `replace_existing` 改为 `true` 才允许覆盖。
- **安装失败后原来的 HACS 还在吗？** 覆盖前会备份旧目录；源码、前端、依赖或安装后复验失败时会尝试回滚。
- **为什么日志要求我手动重启 Home Assistant？** 安装器不会主动重启核心，避免后台静默中断服务；看到成功日志后手动重启即可。
- **运行时还会访问 GitHub 吗？** 安装器关键路径不访问 GitHub、`get.hacs.vip` 或境外下载地址。HACS 安装后的仓库访问由 fork 自带代理负责，稳定性取决于代理实际状态。
- **下载失败怎么办？** 确认 Gitee 和 `pypi.tuna.tsinghua.edu.cn` 可达后重新启动；固定 wheel 有 SHA-256 校验，校验不通过不会安装。
- **这个加载项支持哪些架构？** 只支持 HAOS `amd64` 和 `aarch64`。

## 英文原版

本加载项是自有开发工具，没有独立的英文 README；仓库入口见 [English repository](https://github.com/Treasoni/ha-addon-cn)，上游 fork 见 [HACS China integration](https://gitee.com/hacs-china/integration)。
