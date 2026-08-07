# 中文指南批量生成与审校工作流（zh-guide-workflow）

为仓库中缺失中文指南的 add-on（`addons-manifest.json` 中 `zh_guide: false`）批量生成、门禁、审校、发布中文 README。**核心承诺：每篇指南必须通过「确定性结构门禁 + 审校 subagent 语义核对 + 复验」，并经一次人工确认，才写入 manifest 与 git。** 这就是质量 harness——批量但不失控。

## 范围与排除

- **目标**：`source != local` 且 `zh_guide == false` 且目录存在的 add-on（当前约 147 个；45 个已入库）。
- **排除**：`source: local` 的自有 add-on；同步上游变更（走 `hassio-addon-sync`）；新建 add-on（走脚手架）；单个 add-on 手动翻译（走 `hassio-addon-sync` 中文指南流程）；只读问题。
- 若磁盘 README 已有 `<!-- zh-guide -->` 但 manifest 为 false（desync）→ 不重写，仅标记。

## 前置条件（一次性）

add-on 商店基线已提交 git（`baseline_commit`）。若状态文件 P1 记录的 `baseline_commit` 为空或未验证，先执行主仓库提交（见入口 skill），再继续。

## 目录

- 工作流定义：`.codex/workflows/zh-guide-workflow/`
- 状态文件：`workspace/workflow-runs/zh-guide-batch-{run_id}.workflow.md`
- 门禁脚本：`.codex/scripts/zh-guide-gate.py`
- 审校 subagent：`.claude/agents/zh-guide-reviewer.md`

## Phase 总览

| Phase | 名称 | 工作内容 | todo-state.sh |
|---|---|---|---|
| P0 | 规划与枚举 | 读路由 + `.learnings/`；从 manifest 枚举缺失项；处理 desync；建/续状态文件；与用户确认范围 | start → complete |
| P1 | 同步与基线 | 记录/验证 `baseline_commit`；`sync-addons.py` 预热 `.cache/upstream` 并对账 | start → complete/skip |
| P2 | 批量生成 | 按序（priority-list → 源优先级 → 字母序）为每个缺失 slug 写中文 README | start → complete |
| P3 | 结构门禁 | `zh-guide-gate.py --batch --strict`；机械错误就地修；遗留 → block | start → complete/block |
| P4 | 审校·修复·学习 | 每 slug 调 `zh-guide-reviewer`；修复后重跑门禁复验；结果写批次表 | start → complete/block |
| P5 | 汇总与人工确认 | 汇总 verdict 表；**一次人工确认**才继续 | start → complete/block |
| P6 | 收尾发布 | `--mark-zh` 置 manifest；`--zh-status` 验证；commit；push origin+gitee | start → complete |

## 各 Phase 规则

### P0 规划与枚举
1. 读 `.codex/rules/workflow-routing.md`、`.learnings/RULES.md`、`LEARNINGS.md`、`ERRORS.md`。
2. 从 `addons-manifest.json` 枚举目标：`source != local AND zh_guide == false AND (ROOT/{slug}).is_dir()`。
3. desync 检测：磁盘 README 已有标记但 manifest false → 记为「仅翻转标记」，不进生成队列。
4. 从 `state-template.md` 创建或续用状态文件；每目标一行 `- [ ] {slug}`。
5. 与用户确认：范围（全部 vs `.agents/skills/hassio-addon-sync/guides/priority-list.md` 子集）、严格度（strict vs 宽松）。按本仓库 grilling 约定问清再继续。

### P1 同步与基线
- 状态文件 frontmatter 记录 `baseline_commit`（前置提交的 sha）。
- 运行 `python .codex/scripts/sync-addons.py`（预热 `.cache/upstream/{源}`，对账 manifest；README 永不覆盖，安全）。`.cache/` 已 gitignore。
- 确认无 vendored 目录 dirty（dirty 目录阻塞该 slug 生成，记入 `## 异常记录`）。

### P2 批量生成
- 排序：`.agents/skills/hassio-addon-sync/guides/priority-list.md` 成员在前 → 按源优先级（alexbelgium→official→frenck）→ 字母序。
- 对每个 slug：读 `.cache/upstream/{源}/{slug}/README.md`（上游原版）+ `{slug}/config.yaml` + `CHANGELOG.md`，写中文 `README.md`：
  - 首行 `<!-- zh-guide -->`；
  - 标题 + 一句用途（来自 description）；
  - `## 简介` / `## 安装`（Gitee/GitHub 商店地址）/ `## 配置`（选项表，键用反引号，含类型/默认值）/ `## 使用 / 访问入口`（ingress 或端口）/ `## 常见问题`；
  - 文末 `- 英文原版：[...](上游 raw URL)` + `- 来源仓库：{源}`。
- **护栏**：已有 `<!-- zh-guide -->` 的不重写（直接跳过/desync）。
- 每完成一个，勾选状态文件里对应 `- [ ] {slug}`。

### P3 结构门禁
- `PYTHONIOENCODING=utf-8 python .codex/scripts/zh-guide-gate.py --batch --strict`。
- 机械错误（缺标记/标题/表格、空单元格、占位符、编造键、默认值/类型不符、假端口）由主代理就地修。
- 修完重跑；仍有 FAIL → `todo-state.sh block P3 "<原因>"`，记录 `## 异常记录`。

### P4 审校·修复·学习
- 对每个通过 P3 的 slug，调用 `zh-guide-reviewer` subagent（默认模式，共享工作区）。
- 收到 verdict 后：`pass` → 重跑该 slug 门禁确认 exit 0；`fail` → 看 `UNRESOLVED`，能修就修，需人工判断的收集到 P5；`desync` → 跳过生成，仅标记。
- 把每 slug 结果写入状态文件「批次结果表」：`| slug | source | 生成 | 门禁1 | 审校结论 | 修复项 | 门禁2 | 最终状态 |`。
- 审校 subagent 已直接修复 README 并可能写 `.learnings/`——**不要重复修复，只复验**。

### P5 汇总与人工确认
- 汇总所有 slug 的 verdict 成一张表（通过 / 修复后通过 / 跳过 / 失败）。
- **把汇总表交给用户，人工确认通过后才允许进入 P6。** 用户可驳回个别 slug → 从标记清单移除。

### P6 收尾发布
- `python .codex/scripts/zh-guide-gate.py --mark-zh <通过slugs...>`（脚本复验磁盘标记，无标记拒绝）。
- `python .codex/scripts/sync-addons.py --zh-status` 验证计数（45 → 45+N）。
- `git add -A` → `git commit -m "docs: 新增 N 篇中文使用指南 (...)"`。
- `git push origin main` → `git push gitee main`。**认证失败：把命令与原因报告用户，不重试。**
- 可选：跑 `digest` 做自我学习归档。

## 状态机规则

- phase 状态**只**通过 `.codex/scripts/todo-state.sh` 变更：`start|complete|skip|block <P#n> ["reason"]`。
- 状态文件需含：frontmatter（`workflow_id: zh-guide-workflow`）、`> 当前阶段：` 行、每 phase 唯一状态行 `> [Pn] ⬜ 未开始 {not_started}`、`## 异常记录` 表、`## 最终产出`。
- 复选框与批次结果表由主代理直接写（todo-state.sh 不管理它们）。
- 中断后恢复：读 frontmatter + 当前 phase + 目标清单复选框，从下一个 `⬜` slug 继续。

## 文档

- 领域术语：`CONTEXT.md`。
- 架构决策：`docs/adr/0001-chinese-guide-is-readme.md`（中文指南=README.md；批量=harness 门禁）。
