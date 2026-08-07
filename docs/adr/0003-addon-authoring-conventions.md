# 自有 add-on 编写规范：规范先行、执行后置

仓库现有 192 个 add-on 全部为上游 vendored 镜像，尚无 `source: local` 自有 add-on。用户开始通过 `sync-addons.py --new-addon` 自写 add-on，但仓库没有任何编写规范，且 `templates/new-addon/` 缺 `build.json`（Supervisor 开箱无法构建）。本 ADR 记录：**先把编写标准固化为规范文档，校验脚本、模板修补等执行机制后置到独立工作流**。

Status: accepted

**决策**：新增规则文件 `.claude/rules/common/addon-authoring.md`，作为自有 add-on 编写的唯一规范来源——「先收集资料（上游资料卡）→ config.yaml 必填/options·schema → 目录与文件 → 安全基线 → 验证门禁」，并附 config.yaml 字段表（附录 A）与门禁验收标准清单（附录 B）。规范只定义标准与验收标准，**不实现**校验脚本；`check-addon` 脚本、`templates/new-addon/` 补 `build.json`、以及配套工作流在后续独立任务中按附录 B 落地。`source: local` 判定以 `addons-manifest.json` 的 `source` 字段为准（config.yaml 无 source 字段）。

**Considered Options**：
- 规范 + 脚本 + 模板修补一次交付——执行机制在规范未被验证前就先实现，且与「后续单独建工作流」的计划重叠，放弃。
- 只写规范不产 ADR/术语——丧失决策记录，未来维护者会困惑为何 `build.json` 缺失，放弃。

**Consequences**：
- 规范与执行解耦：工作流可照附录 B 实现门禁，规范不被实现细节污染。
- 模板缺 `build.json` 的问题按本决策后置，随后由 addon-authoring 工作流补齐
  （`templates/new-addon/build.json` 已内置，`check-addon.py` 门禁 C10 校验其覆盖 arch），
  规则与实现现已一致。
- `CONTEXT.md` 新增「上游资料卡」术语；`hassio-addon-sync` 脚手架流程后续应引用本规范。
