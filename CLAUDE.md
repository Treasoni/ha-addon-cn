# Project Instructions

<!-- self-learning:start -->
# homeassistant 自学习规则

## 经验库规则

1. **任务前读取经验库**：执行任何任务前，先读取：
   - `.learnings/RULES.md`：提炼后的铁律
   - `.learnings/LEARNINGS.md`：学习心得
   - `.learnings/ERRORS.md`：错误日志

2. **错误不只记录，还要修源头**：如果同类错误反复出现，或某条规则已写入 `RULES.md` 但仍复发，使用 `maintain-learnings` 追溯并修改对应 skill、模板、hook、校验脚本或项目规则。修复并验证后，才归档或移除活跃记录。

3. **记录要短，规则要可执行**：学习记录写事实和根因；`RULES.md` 写简洁规则，例如"用 X 而非 Y"。不要把 `.learnings/` 变成冗长日志库。

4. **Hook 自动读取**：各 agent profile 通过自己的 hooks 目录运行 `read_learnings.py` 或 `read-learnings.sh`，在会话开始时注入经验库提醒。若 hook 配置不存在，先安装或合并模板中的 hook 配置。

## 推荐触发语

- "记录一下这次学习"
- "把这次错误写进 learnings"
- "learnings 太多了，帮我维护"
- "这个错误又犯了，去修源头"
<!-- self-learning:end -->

<!-- env-template:claude:begin -->
## Environment Variables

- Follow `.claude/rules/common/env.md` whenever creating, updating, migrating, or auditing `.env`, `.env.example`, or environment-variable documentation.
- Keep committed env templates minimal, project-specific, and free of real secrets or machine-local absolute paths.
- After env template changes, run `.claude/scripts/check-env-template.sh`. Use `--strict` when you want unused documented variables to fail the check.
<!-- env-template:claude:end -->

<!-- docker:claude:begin -->
## Docker 规范

- Follow `.claude/rules/common/dockerfile.md` whenever creating, updating, or auditing `Dockerfile`, `build.json`, `build.yaml`, `.dockerignore`, or docker-compose files.
- Reuse templates under `.claude/templates/docker/` for new Dockerfiles; add-on Dockerfiles must stay byte-identical to `.claude/skills/hassio-addon-sync/templates/new-addon/Dockerfile`.
- After Dockerfile/template changes, run `.claude/scripts/check-docker.sh` to verify base-image pinning, non-root user, healthcheck, secrets, exec-form commands, and add-on template consistency.
<!-- docker:claude:end -->

<!-- addon-authoring:claude:begin -->
## Add-on 编写规范

- Follow `.claude/rules/common/addon-authoring.md` whenever creating or maintaining a `source: local` 自有 add-on（脚手架、config.yaml/Dockerfile/run.sh/README、check-addon 门禁）。
- 建目录必须用脚手架：`python .claude/scripts/sync-addons.py --new-addon <slug>`，不得手工建目录/改 manifest；`source: local` 的 add-on 同步脚本永不触碰。
- 动笔前先收集上游资料，落地为 config.yaml 头部 `# === 上游资料卡 ===` 注释块。
- 提交前过门禁：`check-addon.py` 结构+完整度、README 过 `zh-guide-gate.py`、manifest 注册 `source: local`。
<!-- addon-authoring:claude:end -->

<!-- mirror-sources:claude:begin -->
## 国内镜像源（registry proxy 与 image 重写）

- Follow `.claude/rules/common/mirror-sources.md` whenever rewriting `image:` hosts or verifying registry proxies.
- 镜像地址重写只由脚本完成（`rewrite-images.py` / 同步管道），agent 不手工编辑 config.yaml 的 `image:`。
- 验证镜像源：打 manifest 端点 + config.yaml 真实 version，勿用 `tags/list`、勿用 `latest`。
- 不碰 `source: local`、不碰 `build.json` 的 `build_from`、不改写官方 add-on。
<!-- mirror-sources:claude:end -->

<!-- prompt-cache-bootstrap:claude:begin -->
## Prompt Cache

- Follow `.claude/rules/common/prompt-cache.md` for high-frequency prompt design.
- Keep stable instructions and output formats before dynamic user input, file excerpts, dates, IDs, and runtime state.
- Reuse canonical templates and load long context only when needed.
<!-- prompt-cache-bootstrap:claude:end -->

<!-- workflow-todo-state:start -->
## Workflow Todo State

Named workflow state files are the source of truth for every routed workflow.

- Workflow definitions live under `.claude/workflows/{workflow-id}/`.
- Workflow state files live under `workspace/workflow-runs/` and should be named after the task, for example `payment-refactor.workflow.md`.
- Before any action that changes project files, runs project commands, or calls external services, read `.claude/rules/workflow-routing.md` and match the user's original request against its triggers and exclusions.
- When a `Required: yes` workflow matches, read its `workflow.md`, create or resume its state file, and start the current phase before doing the work. Do not take the ordinary execution path instead.
- If the route is ambiguous, ask the user before acting.
- Read the active workflow state file before starting any phase; do not skip prerequisite phases.
- Change phase state only through `.claude/scripts/todo-state.sh`.
- Use one unique phase status line per phase, for example `> [P0] ⬜ 未开始`.
- On resume after interruption, inspect the YAML frontmatter and current phase before acting.
- Each workflow directory must contain a `routing.yaml`. After creating, changing, renaming, or deleting a workflow, run `.claude/scripts/sync-workflow-routing.sh`; the update is incomplete until `.claude/scripts/sync-workflow-routing.sh --check` passes.
<!-- workflow-todo-state:end -->
