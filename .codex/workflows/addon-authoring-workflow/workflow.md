# 自有 add-on 开发工作流（addon-authoring-workflow）

从零开发或维护 `source: local` 自有 add-on：脚手架建目录、先收集上游资料（上游资料卡）、编写 config.yaml / Dockerfile / run.sh / 中文 README、过 `check-addon` 结构门禁、审校复验、一次人工确认后发布。**核心承诺：每个 `source: local` 自有 add-on 必须依次通过「先收集资料（上游资料卡）→ 编写实现 → check-addon 结构门禁 → 审校复验 → 一次人工确认」才能发布。** 这就是质量 harness——从零编写但不失控。

## 范围与排除

- **目标**：新建或维护 `source: local` 自有 add-on（判定以 `addons-manifest.json` 的 `source` 字段为准，config.yaml 无 `source` 字段）。
- **排除**：同步上游 add-on（走 `hassio-addon-sync`）；批量中文指南（走 `zh-guide-workflow`）；单个 add-on 手动翻译；只读问题。
- 规范强制「先收集资料再写」：未完成上游资料卡不得编写 options。

## 前置条件

规范文件 `.codex/rules/common/addon-authoring.md` 存在（定义标准与附录 A/B 验收清单）；worktree/分支基线已提交 git（`baseline_commit`）。若状态文件 P0 记录的 `baseline_commit` 为空或未验证，先提交基线再继续。

## 目录

- 工作流定义：`.codex/workflows/addon-authoring-workflow/`
- 状态文件：`workspace/workflow-runs/addon-authoring-{slug}.workflow.md`
- 门禁脚本：`.codex/scripts/check-addon.py`
- 审校 subagent：`.claude/agents/addon-authoring-reviewer.md`
- 规范：`.codex/rules/common/addon-authoring.md`

## Phase 总览

| Phase | 名称 | 工作内容 | todo-state.sh |
|---|---|---|---|
| P0 | 规划与确认 | 读路由 + `.learnings/`；与用户确认 slug/name/version/上游 URL；建状态文件；确认 build.json 由脚手架生成 | start → complete |
| P1 | 脚手架与资料收集 | `sync-addons.py --new-addon` 建目录；收集上游官方资料 → 填 config.yaml「上游资料卡」；确认无 image、build.json 生成 | start → complete |
| P2 | 编写实现 | 按资料卡写 config.yaml / Dockerfile / run.sh / 中文 README | start → complete |
| P3 | 结构门禁 | `check-addon.py <slug>`；机械错误就地修；遗留 → block | start → complete/block |
| P4 | 审校复验 | 调 `addon-authoring-reviewer` 语义核对；修复后重跑 `check-addon.py` 复验 | start → complete/block |
| P5 | 汇总与人工确认 | 汇总 verdict 表；**一次人工确认**才继续 | start → complete/block |
| P6 | 收尾发布 | 复验 manifest `source==local`/`local_version`；commit；push origin | start → complete |

## 各 Phase 规则

### P0 规划与确认
1. 读 `.codex/rules/workflow-routing.md`、`.learnings/RULES.md`、`LEARNINGS.md`、`ERRORS.md`。
2. 与用户确认：`slug`、`name`、`version`、上游软件 URL。按本仓库 grilling 约定问清再继续。
3. 从 `state-template.md` 创建状态文件（`addon-authoring-{slug}.workflow.md`），frontmatter 记录 `{task}`/`{slug}`。
4. 确认模板已内置 `build.json`（`build_from` 覆盖 arch），脚手架（P1）会原样带入，无需手工补。

### P1 脚手架与资料收集
- 运行 `python .codex/scripts/sync-addons.py --new-addon <slug> [--name ...] [--version ...]`（skill：`hassio-addon-sync`）。**不得手工建目录、手工改 manifest。**
- 收集上游软件官方资料（功能与用途、监听端口、默认账号/初始密码、需持久化的数据目录、运行所需环境变量、官方版本）→ 填入 config.yaml 头部「上游资料卡」注释块（`# === 上游资料卡 ===`，见规范）。**先收集资料再写；未收集完成不得编写 options。**
- 确认 config.yaml 无 `image:` 字段、`build.json` 已生成（`build_from` 每 arch 指向 base 镜像）。

### P2 编写实现
- 按资料卡写 config.yaml：`url` 为真实主页、`description` 中文非占位符、`options`/`schema` 键一一对应、schema 类型合法（见规范附录 A）。
- Dockerfile / run.sh 与 config 一致：`run.sh` 用 `bashio::config` 读取的键必须存在于 `options`；`Dockerfile` 用 `ARG BUILD_FROM` + `CMD ["/run.sh"]`。
- 写中文 README：首行 `<!-- zh-guide -->`，含 `## 简介` / `## 安装` / `## 配置`（配置表键用反引号，含类型/默认值）/ `## 使用 / 访问入口` / `## 常见问题`。

### P3 结构门禁
- `PYTHONIOENCODING=utf-8 python .codex/scripts/check-addon.py <slug>`。
- 机械错误（缺字段/占位符/options·schema 键不一致/类型非法/build.json 缺失/误带 image）由主代理就地修。
- 修完重跑；仍有 FAIL → `todo-state.sh block P3 "<原因>"`，记录 `## 异常记录`。

### P4 审校复验
- 调用 `addon-authoring-reviewer` subagent（默认模式，共享工作区），核对 config.yaml 的 `options`/`schema` 与「上游资料卡」+ 上游官方资料一致（端口/默认账号/数据目录/env 真实）、`description` 真实非编造、`run.sh` 引用的键存在、README 与 config 一致、`build.json` 覆盖 `arch`。
- 收到 verdict 后：`pass` → 重跑 `check-addon.py <slug>` 确认 exit 0；`fail` → 看 `UNRESOLVED`，能修就修，需人工判断的收集到 P5。
- 审校 subagent 已直接修复实现文件并可能写 `.learnings/`——**不要重复修复，只复验**。结果写入状态文件「审校结果」表。

### P5 汇总与人工确认
- 汇总 verdict 成一张表（通过 / 修复后通过 / 失败）。
- **把汇总表交给用户，人工确认通过后才允许进入 P6。** 用户可驳回个别点 → 回到对应阶段修复。

### P6 收尾发布
- 复验 `addons-manifest.json` 中该 slug `source == "local"` 且 `local_version` 正确。
- `git add -A` → `git commit -m "feat: 新增 source: local 自有 add-on {slug} (...)"`。
- `git push origin main` → `git push gitee main`。**认证失败：把命令与原因报告用户，不重试。**
- 可选：跑 `digest` 做自我学习归档。

## 状态机规则

- phase 状态**只**通过 `.codex/scripts/todo-state.sh` 变更：`start|complete|skip|block <P#n> ["reason"]`。
- 状态文件需含：frontmatter（`workflow_id: addon-authoring-workflow`）、`> 当前阶段：` 行、每 phase 唯一状态行 `> [Pn] ⬜ 未开始 {not_started}`、`## 异常记录` 表、`## 最终产出`。
- 复选框与审校结果表由主代理直接写（todo-state.sh 不管理它们）。
- 中断后恢复：读 frontmatter + 当前 phase + 复选框，从下一个 `⬜` phase 继续。

## 文档

- 领域术语：`CONTEXT.md`（上游资料卡 / `source: local`）。
- 架构决策：`docs/adr/0003-addon-authoring-conventions.md`（规范先行、执行后置）。
- 规范：`.codex/rules/common/addon-authoring.md`（附录 A 字段表 / 附录 B 门禁清单）。
