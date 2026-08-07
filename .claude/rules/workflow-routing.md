# Workflow Routing

Use this rule file to decide which named workflow to use and where to find active run state.

## Workflow Directory Layout

```text
.claude/workflows/{workflow-id}/workflow.md        # workflow definition
.claude/workflows/{workflow-id}/state-template.md # state file template
workspace/workflow-runs/*.workflow.md                   # active or historical run state
```

## Available Workflows

<!-- workflow-routing:generated:start -->
| Workflow ID | Required | When To Use | Positive Triggers | Excludes | Definition | State File Pattern |
| --- | --- | --- | --- | --- | --- | --- |
| `zh-guide-workflow` | yes | 批量生成、审校或补充缺失的中文 add-on 指南（zh_guide=false 的 add-on） | 生成中文指南; 批量生成中文指南; 补充中文指南; 审校中文指南; zh-guide; 补全中文 | 同步 add-on; 新建 add-on; 单个 add-on 手动翻译; 只读问题 | `.claude/workflows/zh-guide-workflow/workflow.md` | `workspace/workflow-runs/zh-guide-batch-{run_id}.workflow.md` |
<!-- workflow-routing:generated:end -->

## Routing Rules

- Before any action that changes project files, runs project commands, or calls external services, choose the matching `workflow_id` from the table.
- Match the user's original request against positive triggers and exclusions. A matching `Required: yes` workflow cannot use the ordinary execution path.
- If multiple workflows match, choose the more specific workflow; if the route remains ambiguous, ask the user before acting.
- If a matching run already exists under `workspace/workflow-runs/`, resume it instead of creating a duplicate.
- If no run exists, create a named state file from the workflow's `state-template.md`.
- Name state files after the task or feature, not `todo.md`, unless the project has exactly one workflow.
- Every phase must read the active state file before acting.
- Phase state must be changed only through `.claude/scripts/todo-state.sh`.
- Each workflow directory must have a `routing.yaml`; it is the source of truth for the generated table above.
- After creating, changing, renaming, or deleting a workflow, run `.claude/scripts/sync-workflow-routing.sh`. Use `.claude/scripts/sync-workflow-routing.sh --check` in pre-commit or CI.

## Active Runs

| State File | Workflow ID | Task | Current Phase | Status | Notes |
| --- | --- | --- | --- | --- | --- |
| | | | | | |
