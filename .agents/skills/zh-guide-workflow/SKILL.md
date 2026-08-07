---
name: zh-guide-workflow
description: 批量生成、审校或补充缺失的中文 add-on 使用指南，通过确定性结构门禁 + 审校 subagent 保证质量。触发词：生成中文指南、批量生成中文指南、补充中文指南、审校中文指南、中文说明、zh-guide、补全中文。排除：同步 add-on、新建 add-on、单个 add-on 手动翻译、只读问题。
---

# 中文指南批量生成与审校

本 skill 是 `zh-guide-workflow` 工作流的**入口**。收到触发请求时，按下面的分发规则路由到该工作流，由工作流状态机驱动 P0–P6。

## 触发与排除

**触发**：生成中文指南；批量生成中文指南；补充中文指南；审校中文指南；中文说明；zh-guide；补全中文。

**排除（转到 `hassio-addon-sync`）**：
- 同步 add-on / 更新上游（→ 同步流程）
- 新建自有 add-on（→ 脚手架流程）
- 单个 add-on 手动翻译（→ 中文指南流程，不进本工作流）
- 只读问题（→ 直接回答）

## 分发规则（遵循 AGENTS.md + workflow-todo-state）

1. **读经验库**：`.learnings/RULES.md`、`LEARNINGS.md`、`ERRORS.md`。
2. **路由匹配**：读 `.codex/rules/workflow-routing.md`，把用户请求对照 `zh-guide-workflow` 的 triggers/excludes。匹配且 `Required: yes` → **必须走本工作流**，不得走普通执行路径。
3. **建/续状态文件**：
   - 若 `workspace/workflow-runs/zh-guide-batch-{run_id}.workflow.md` 已存在且任务匹配 → 续用（读 frontmatter + 当前 phase，从中断处继续）。
   - 否则从 `.codex/workflows/zh-guide-workflow/state-template.md` 创建，`run_id` 用当天日期（如 `2026-08-07`）。
4. **宣布并开始**：向用户宣布 `workflow_id=zh-guide-workflow`、状态文件路径、当前 phase；然后 `bash .codex/scripts/todo-state.sh <state-file> start P0`。
5. **范围歧义**：若请求范围模糊（全部缺失 vs `.agents/skills/hassio-addon-sync/guides/priority-list.md` 子集；strict vs 宽松），先按本仓库 grilling 约定问清，再让 P0 完成。

## 前置条件检查

- 若工作流尚未跑过，检查 `baseline_commit`：add-on 商店基线必须已提交 git（见 `workflow.md` 前置条件）。未提交则说明用户在**主仓库**执行一次提交：
  ```bash
  # 在主仓库 C:\homeassistant
  python .codex/scripts/sync-addons.py
  git add -A && git commit -m "store: vendored add-on store baseline + manifest"
  git push origin main && git push gitee main
  # 然后本 worktree 分支 reset --hard main
  ```

## 与既有技能的分工

- `hassio-addon-sync`：同步上游、新建 add-on、**单个** add-on 手动翻译。
- 本 skill / `zh-guide-workflow`：**批量**生成 + 审校 + 门禁 + 发布，取代旧的手动批量护栏（见 `docs/adr/0001-chinese-guide-is-readme.md`）。

## 质量承诺（harness）

每篇指南必须过：确定性结构门禁（`zh-guide-gate.py`）→ 审校 subagent 对照 config.yaml 语义核对并修复 → 复验 → 一次人工确认 → 才写 manifest 与 git。不达标不放行。
