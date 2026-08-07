---
name: addon-authoring
description: 从零开发或维护 source: local 自有 add-on：脚手架建目录、先收集上游资料（上游资料卡）、编写 config.yaml/Dockerfile/run.sh/中文 README、过 check-addon 门禁与审校复验、一次人工确认后发布。触发词：新建 add-on、开发 add-on、编写 add-on、写 add-on、创建 add-on、生成 add-on、add-on 脚手架、开发自有 add-on、自有 add-on。排除：同步 add-on、审校中文指南、批量中文指南、单个 add-on 手动翻译、只读问题。
---

# 自有 add-on 开发

本 skill 是 `addon-authoring-workflow` 工作流的**入口**。收到触发请求时，按下面的分发规则路由到该工作流，由工作流状态机驱动 P0–P6。

## 触发与排除

**触发**：新建 add-on；开发 add-on；编写 add-on；写 add-on；创建 add-on；生成 add-on；add-on 脚手架；开发自有 add-on；自有 add-on。

**排除（转到对应流程）**：
- 同步 add-on / 更新上游（→ `hassio-addon-sync` 同步流程）
- 审校中文指南 / 批量中文指南（→ `zh-guide-workflow`）
- 单个 add-on 手动翻译（→ `hassio-addon-sync` 中文指南流程）
- 只读问题（→ 直接回答）

## 分发规则（遵循 AGENTS.md + workflow-todo-state）

1. **读经验库**：`.learnings/RULES.md`、`LEARNINGS.md`、`ERRORS.md`。
2. **路由匹配**：读 `.codex/rules/workflow-routing.md`，把用户请求对照 `addon-authoring-workflow` 的 triggers/excludes。匹配且 `Required: yes` → **必须走本工作流**，不得走普通执行路径。
3. **建/续状态文件**：
   - 若 `workspace/workflow-runs/addon-authoring-{slug}.workflow.md` 已存在且任务匹配 → 续用（读 frontmatter + 当前 phase，从中断处继续）。
   - 否则从 `.codex/workflows/addon-authoring-workflow/state-template.md` 创建。
4. **宣布并开始**：向用户宣布 `workflow_id=addon-authoring-workflow`、状态文件路径、当前 phase；然后 `bash .codex/scripts/todo-state.sh <state-file> start P0`。
5. **范围歧义**：若 slug/name/version/上游软件 URL 未定，先按本仓库 grilling 约定问清，再让 P0 完成。

## 前置条件检查

- 规范文件 `.codex/rules/common/addon-authoring.md` 必须存在（定义标准与附录 A/B 验收清单）。
- 若工作流尚未跑过，检查 `baseline_commit`：add-on 商店基线必须已提交 git（见 `workflow.md` 前置条件）。

## 与既有技能的分工

- `hassio-addon-sync`：同步上游、**单个** add-on 手动翻译、快速脚手架建目录（`sync-addons.py --new-addon`）。
- 本 skill / `addon-authoring-workflow`：**新建/维护 source: local 自有 add-on**，质量门禁（资料卡 → 编写 → check-addon → 审校 → 人工确认 → 发布）。快速脚手架只建目录，**发布前必须过 `python .codex/scripts/check-addon.py <slug>`**。
- `zh-guide-workflow`：批量中文指南（`zh_guide=false` 的 vendored add-on），与新建自有 add-on 互斥。

## 质量承诺（harness）

每个自有 add-on 必须过：先收集资料（config.yaml 头部「上游资料卡」注释块）→ 编写 config.yaml / Dockerfile / run.sh / 中文 README → 确定性结构门禁（`check-addon.py` C1–C10）→ 审校 subagent（`addon-authoring-reviewer`）语义核对并修复 → 复验 → 一次人工确认 → 才发布（commit + push 双远程）。不达标不放行。
