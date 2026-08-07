# 自有 add-on 编写规范（addon-authoring）

---
paths:
  - ".codex/scripts/sync-addons.py"
  - ".agents/skills/hassio-addon-sync/templates/new-addon/**"
  - "addons-manifest.json"
---

本规则规范「新建自有 add-on（`source: local`）」的编写。`source: local` 的判定以
`addons-manifest.json` 的 `addons[slug].source` 为准——**config.yaml 里没有 `source` 字段**。
本规则是**规范文档**：只定义标准与门禁验收标准；校验脚本、模板修补与配套工作流由后续任务
按附录 B 实现。

## 适用范围与总则

- 适用对象：`source: local` 自有 add-on。vendored add-on（`alexbelgium | official | frenck`）
  由同步脚本管理，不在本规则范围（见 `CONTEXT.md`「vendored add-on」）。
- **建目录必须用脚手架**：`python .codex/scripts/sync-addons.py --new-addon <slug>`
  （skill：`hassio-addon-sync`）。不得手工建目录、手工改 manifest。
- **写保护**：`source: local` 的 add-on 同步脚本、镜像改写、批量中文指南**永不触碰**
  （见 `mirror-sources.md` 与 hassio-addon-sync 禁止事项 #6）。
- **README 即中文指南**：中文 README 就是 add-on 的 `README.md` 本身，首部带
  `<!-- zh-guide -->` 标记（ADR-0001）。

## 写前必做：先收集资料（强制）

动笔前必须完成以下收集，产出**上游资料卡**；未收集完成不得编写 Dockerfile 与 options。

1. **上游软件官方资料**（官方文档 / GitHub / Docker Hub）：
   - 功能与用途一句话；项目主页（`url`）；
   - 监听端口（协议 + 默认端口）；
   - 默认账号 / 初始密码（若有，标注「安装后需改」）；
   - 需持久化的数据目录；
   - 运行所需环境变量；
   - 官方镜像 tag 与版本号（作为 `version` 参照）。
2. **对照本规则附录 A** 的 config.yaml 字段表，确认要用到的字段与 schema 类型。

落地物：config.yaml 头部 `# === 上游资料卡 ===` 注释块，记录上述要点与来源 URL：

```yaml
# === 上游资料卡 ===
# upstream: https://github.com/xxx/yyy   # 软件项目主页
# ports: 8123/tcp                        # 默认端口
# default_credentials: admin / 安装后首次进入修改
# data_dir: /data                        # 需持久化的目录
# env_vars: AUTH_KEY                     # 运行所需环境变量
# version: 2.5.0                         # 参照的上游版本
```

## config.yaml 必填规范（最小骨架）

- **必填字段**：`name`、`version`、`slug`、`description`、`url`、`arch`、`startup`、`boot`、
  `options`、`schema`。
  - `name`：显示名（中文或软件原名均可）。
  - `version`：**引号包裹**，语义化版本（`"1.2.3"`）。
  - `slug`：`[a-z0-9][a-z0-9_-]*`，必须与 manifest 注册的 slug 一致。
  - `description`：中文一句话用途，**不得是占位符**（`在这里写`/`待补充`/`TODO`/lorem）。
  - `url`：上游软件项目主页。
  - `arch`：默认含 `aarch64`/`amd64`（模板标准，base 镜像已实测可用）；合法平台
    `{aarch64, amd64, armv7, armhf, i386}`。需要更多平台时手工添加，并验证对应
    `{arch}-base` 镜像 tag（注意：HA 已停发 armv7 base，版本止于 `3.22-2025.11.1`）。
  - `startup`/`boot`：`application` + `auto`；需手动启停用 `boot: manual`。
- **`init: false`** 为惯例默认（无需 supervisor init 时显式声明）。
- **禁止 `image:` 字段**：本地 add-on 本地构建，镜像由 Dockerfile/build 文件产出，
  来源以 manifest 为准；镜像地址重写不适用于本地 add-on。
- **`build.json` 必带**：Supervisor 本地构建依赖，`build_from` 为每个 `arch` 指向
  `ghcr.io/home-assistant/{arch}-base`。模板已内置（`templates/new-addon/build.json`），
  脚手架原样带入。

## options/schema 设计规范

- 键名：**小写下划线**（snake_case）。
- 类型选择（schema 合法类型）：`str`、`int`、`float`、`bool`、`port`、`password`、
  `match(^...$)`（正则）、`list`、`dict`，以及 `|` 联合（`str|int`）、`?` 可选
  （`int?`）、`list(...)` 枚举（`list(trace|debug|info)?`）。
- **有 `options` 就必须有 `schema`**，且两者键**一一对应**（缺一不可）。
- 无用户配置的 add-on 可省略 `options`/`schema`（上游已有先例）。
- **密码/密钥**字段：schema 类型用 `password`，options 默认值留空由用户填写，
  不得放真实明文密码。
- 默认值必须是**真实可用**的值，不得用占位符（`hello world`/`example`/`changeme`）。

## 目录与文件规范

- 新 add-on 目录必含：`config.yaml`、`build.json`、`Dockerfile`、`run.sh`、
  `README.md`（中文指南）；建议补 `icon.png`/`logo.png`。
- `Dockerfile`：`ARG BUILD_FROM` + `FROM $BUILD_FROM`，`ENV LANG C.UTF-8`，
  `CMD ["/run.sh"]`，入口脚本加执行权限。
- `run.sh`：`#!/usr/bin/with-contenv bashio`，`set -e`，用 `bashio::config` 读 options，
  长驻进程用 `exec ... --foreground`。
- 不得引入上游工具链噪音（`apparmor.txt`/`updater.json`/`stats.png` 等是 vendored
  alexbelgium 产物，本地 add-on 不需要）。

## 安全基线

- **非必要不以 root 运行**；`privileged`、`host_network`、`host_dbus` 仅在确有必要时使用，
  并在资料卡或 README 说明原因。
- 密码/密钥用 `password` 类型、默认值为空；**不硬编码密钥**进 Dockerfile/run.sh/options。
- 临时文件放容器临时目录并在退出清理；`set -e` 防静默失败。
- 只暴露必需端口，`ports_description` 说明每个端口用途。

## 验证与门禁（验收标准）

提交前必须满足以下验收标准（校验脚本/工作流按附录 B 执行）：

1. config.yaml 通过**结构 + 完整度门禁**（附录 B 清单全绿）。
2. README 通过 `zh-guide-gate.py` 结构章节（`简介/安装/配置/使用/常见问题`、配置表无空
   单元格、无占位符）。
3. `addons-manifest.json` 已注册 `source: local`，`slug`/`local_version` 正确。
4. 改动只涉及本 add-on 目录与 manifest，未触碰任何 vendored add-on。

## 附录 A：config.yaml 字段表

| 字段 | 说明 | 本地 add-on |
|---|---|---|
| `name` | 显示名 | 必填 |
| `version` | 版本号（引号包裹，语义化） | 必填 |
| `slug` | 唯一标识，`[a-z0-9][a-z0-9_-]*` | 必填 |
| `description` | 中文一句话，非占位符 | 必填 |
| `url` | 上游项目主页 | 必填 |
| `arch` | 支持的架构列表 | 必填 |
| `options` | 用户配置默认值 | 有配置时必填 |
| `schema` | options 的校验声明 | 有 options 时必填 |
| `startup` | `application`/`services`/`system`/`initialize`/`once` | 必填 |
| `boot` | `auto`/`manual` | 必填 |
| `init` | `false`（默认）/`true` | 惯例 `false` |
| `image` | 预构建镜像引用 | **禁止**（本地构建） |
| `build.json` | 本地构建声明（`build_from` 每 arch） | 必填（模板已内置） |
| `map` | 挂载路径（`addon_config:rw` 等） | 按需 |
| `ports` / `ports_description` | 端口映射 + 用途 | 按需 |
| `ingress` / `ingress_port` / `ingress_stream` | Web UI 内嵌 | 按需 |
| `host_network` / `host_dbus` | 主机网络 / D-Bus | 慎用 |
| `hassio_api` / `hassio_role` / `homeassistant_api` / `auth_api` | Supervisor/HA 接口权限 | 按需 |
| `uart` / `video` / `audio` / `devices` / `privileged` | 硬件/设备访问 | 慎用 |
| `panel_icon` / `panel_title` | 侧栏面板 | 按需 |
| `backup_exclude` | 备份排除路径 | 按需 |
| `environment` | 固定环境变量 | 按需 |
| `homeassistant` | 最低 HA 版本 | 按需 |

## 附录 B：门禁验收标准清单（供校验脚本/工作流实现）

- slug 目录存在，且 manifest 中 `source == "local"`（否则拒绝）。
- config.yaml 可解析；必填字段齐全（见「config.yaml 必填规范」）。
- config.yaml 头部含 `# === 上游资料卡 ===` 注释块（先收集资料已落地）。
- `description` 非占位符（`在这里写`/`待补充`/`TODO`/lorem）。
- `version` 引号包裹且非空；`arch` 非空且 ∈ 合法平台。
- `options` 与 `schema` 键完全一致；schema 类型合法（附录 A 类型枚举 + `|`/`?`/`list(..)`/`match(..)`）。
- 本地 add-on 无 `image:` 字段。
- `build.json` 存在且 `build_from` 覆盖 config.yaml 声明的每个 arch。
- 有 `options` 必有 `schema`。
