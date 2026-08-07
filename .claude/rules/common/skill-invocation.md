# Skill Invocation

## 技能列表
<!-- skill-registry:managed ["addon-authoring","ask-matt","claude-handoff","code-review","codebase-design","diagnosing-bugs","digest","domain-modeling","git-guardrails-claude-code","grill-me","grill-with-docs","grilling","handoff","hassio-addon-sync","implement","improve-codebase-architecture","loop-me","maintain-learnings","manifest-platform","migrate-to-shoehorn","prompt-cache-optimizer","prototype","research","resolving-merge-conflicts","scaffold-exercises","security-secret-audit","setup-matt-pocock-skills","setup-pre-commit","setup-ts-deep-modules","sync-skill-registry","tdd","teach","to-questionnaire","to-spec","to-tickets","triage","wait-what","wayfinder","wizard","workflow-todo-state","writing-beats","writing-for-agents","writing-fragments","writing-shape","zh-guide-workflow"] -->

#### 未分类

| 技能 | 触发场景 | 关键触发词 |
|------|----------|-----------|
| `addon-authoring` | 从零开发或维护 source: local 自有 add-on：脚手架建目录、先收集上游资料（上游资料卡）、编写 config.yaml/Dockerfi… | 新建 add-on、开发 add-on、编写 add-on、写 add-on、创建 add-on、生成 add-on、add-on 脚手架、开发自有 add-on、自有 add-on。排除：同步 add-on、审校中文指南、批量中文指南、单个 add-on 手动翻译、只读问题 |
| `ask-matt` | Ask which skill or flow fits your situation. A router over the skills in this… | Ask which skill or flow fits your situat… |
| `claude-handoff` | Hand the current conversation off to a fresh background agent that picks up t… | Hand the current conversation off to a f… |
| `code-review` | Review the changes since a fixed point (commit, branch, tag | review since X |
| `codebase-design` | Shared vocabulary for designing deep modules. Use when the user wants to desi… | Shared vocabulary for designing deep mod… |
| `diagnosing-bugs` | Diagnosis loop for hard bugs and performance regressions. Use when the user s… | diagnose、debug this |
| `digest` | 自我学习阶段。回顾本次会话，记录真实发生的学习点和错误到 .learnings/； | 自我学习阶段 |
| `domain-modeling` | Build and sharpen a project's domain model. Use when the user wants to pin do… | Build and sharpen a project's domain mod… |
| `git-guardrails-claude-code` | Set up Claude Code hooks to block dangerous git commands (push, reset --hard | Set up Claude Code hooks to block danger… |
| `grill-me` | A relentless interview to sharpen a plan or design. | A relentless interview to sharpen a plan… |
| `grill-with-docs` | A relentless interview to sharpen a plan or design | A relentless interview to sharpen a plan… |
| `grilling` | Grill the user relentlessly about a plan, decision | Grill the user relentlessly about a plan… |
| `handoff` | Compact the current conversation into a handoff document for another agent to… | Compact the current conversation into a … |
| `hassio-addon-sync` | 维护本仓库的 Home Assistant Add-on 商店：同步上游 add-on 变更、生成中文使用指南、从模板新建自有 add-on。 | 同步 add-on、更新上游、add-on 商店、生成中文指南、新建 add-on、sync addons |
| `implement` | "Implement a piece of work based on a spec or set of tickets." | Implement a piece of work based on a spec or set of tickets. |
| `improve-codebase-architecture` | Scan a codebase for deepening opportunities | Scan a codebase for deepening opportunit… |
| `loop-me` | Grill me about specs for the workflows I want to build, within this workspace. | Grill me about specs for the workflows I… |
| `maintain-learnings` | 维护 .learnings/ 经验库，把过多或反复出现的学习记录、错误日志、规则失效问题聚类诊断，追溯并修改对应 skill、模板、hook、校验脚本或项目规则； | 维护 .learnings/ 经验库，把过多或反复出现的学习记录、错误日志、规则… |
| `manifest-platform` | Install, configure, migrate, and validate a portable manifest registry for ag… | Install, configure, migrate, and validat… |
| `migrate-to-shoehorn` | Migrate test files from `as` type assertions to @total-typescript/shoehorn. U… | Migrate test files from `as` type assert… |
| `prompt-cache-optimizer` | 审计并优化 LLM 提示缓存命中率、输入 token、延迟与调用成本。 | 优化缓存命中、降低 token 成本、审计 LLM 调用、提示词缓存优化、优化 AI 调用费用 |
| `prototype` | Build a throwaway prototype to answer a design question. Use when the user wa… | Build a throwaway prototype to answer a … |
| `research` | Investigate a question against high-trust primary sources and capture the fin… | Investigate a question against high-trus… |
| `resolving-merge-conflicts` | "Use when you need to resolve an in-progress git merge/rebase conflict." | Use when you need to resolve an in-progress git merge/rebase conflict. |
| `scaffold-exercises` | Create exercise directory structures with sections, problems, solutions | Create exercise directory structures wit… |
| `security-secret-audit` | Audit a Git repository for exposed API keys, tokens, passwords, private keys | Audit a Git repository for exposed API k… |
| `setup-matt-pocock-skills` | Configure this repo for the engineering skills — set up its issue tracker | Configure this repo for the engineering … |
| `setup-pre-commit` | Set up Husky pre-commit hooks with lint-staged (Prettier), type checking | Set up Husky pre-commit hooks with lint-… |
| `setup-ts-deep-modules` | Wire dependency-cruiser into a TypeScript repo so each package is a deep modu… | Wire dependency-cruiser into a TypeScrip… |
| `tdd` | Test-driven development. Use when the user wants to build features or fix bug… | red-green-refactor |
| `teach` | Teach the user a new skill or concept, within this workspace. | Teach the user a new skill or concept, w… |
| `to-questionnaire` | Turn a decision you can't fully answer into a questionnaire for someone else … | Turn a decision you can't fully answer i… |
| `to-spec` | Turn the current conversation into a spec and publish it to the project issue… | Turn the current conversation into a spe… |
| `to-tickets` | Break a plan, spec, or the current conversation into a set of tracer-bullet t… | Break a plan, spec, or the current conve… |
| `triage` | Move issues and external PRs through a state machine of triage roles — catego… | Move issues and external PRs through a s… |
| `wait-what` | Stop. That last message did not land — re-pitch it. | Stop |
| `wayfinder` | Plan a huge chunk of work — more than one agent session can hold — as a share… | Plan a huge chunk of work — more than on… |
| `wizard` | Generate an interactive bash wizard that walks a human through steps only the… | Generate an interactive bash wizard that… |
| `workflow-todo-state` | Create or retrofit reusable named workflow state machines for multi-step agen… | Create or retrofit reusable named workfl… |
| `writing-beats` | Writing, exploit — assemble raw material into a journey of beats | Writing, exploit — assemble raw material… |
| `writing-for-agents` | Writing documents for agents. Use when creating or editing skills | Writing documents for agents |
| `writing-fragments` | Writing, explore — mine raw fragments, no structure yet. | Writing, explore — mine raw fragments, n… |
| `writing-shape` | Writing, exploit — shape raw material into an article, paragraph by paragraph. | Writing, exploit — shape raw material in… |
| `zh-guide-workflow` | 批量生成、审校或补充缺失的中文 add-on 使用指南，通过确定性结构门禁 + 审校 subagent 保证质量。 | 生成中文指南、批量生成中文指南、补充中文指南、审校中文指南、中文说明、zh-guide、补全中文。排除：同步 add-on、新建 add-on、单个 add-on 手动翻译、只读问题 |

#### 工具发现

| 技能 | 触发场景 | 关键触发词 |
|------|----------|-----------|
| `sync-skill-registry` | 技能注册表同步工具。扫描任意 agent skill 目录中的 */SKILL.md 并自动更新对应 skill-invocation.md 中的技能列表… | 同步注册表、更新技能列表、sync skill registry、update skill registration、刷新技能列表、同步技能表格 |

### 1. 分析意图

根据用户请求选择最合适的可复用 skill 或模板。
