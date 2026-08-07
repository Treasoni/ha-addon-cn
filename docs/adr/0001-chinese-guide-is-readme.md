# 中文指南 = 已提交的 README.md，批量产出由 harness 门禁把关

本仓库的中文使用指南就是 add-on 的 `README.md` 本身（HA 详情页直接渲染它），通过首部 `<!-- zh-guide -->` 标记识别，不另建 `README_zh` 之类的独立文件；批量生成的中文指南不再受"禁止一次性生成全部"护栏限制，而是通过确定性结构门禁 + 审校 subagent 语义核对 + 复验 + 人工确认这一 harness 管线来保证质量。

Status: accepted

**Considered Options**：
- 独立 `README_zh.md` 文件——与 HA 渲染机制冲突，需额外接线，放弃。
- 手动逐个翻译（`hassio-addon-sync` 原流程）——质量靠人肉，无法支撑 ~147 篇的批量任务，保留给单个 add-on 场景。
- 批量不经审校直接生成——违背原"禁止批量 200+"护栏，被 harness 门禁取代。

**Consequences**：批量生成成为安全默认路径；旧护栏"不要一次性批量生成全部"已放宽为"必须全部通过 harness 门禁与一次人工确认"。入口 skill（`.claude/skills/zh-guide-workflow/SKILL.md`）交叉引用本文；`hassio-addon-sync/SKILL.md` 的旧护栏文本因该技能位于主仓库、随商店基线一并提交，其第 70 行「不要一次性批量生成全部 200+ 篇未经审阅的指南」需在提交时手工更新为指向本文。
