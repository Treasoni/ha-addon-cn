---
workflow_id: zh-guide-workflow
workflow_name: 中文指南批量生成与审校
workflow_version: 1
state_file_type: workflow-run
run_id: "{run_id}"
task: "{task}"
created_from: ".codex/workflows/zh-guide-workflow/state-template.md"
created_at: "{date}"
last_updated: "{date}"
current_phase: P0
current_status: not_started
mode: standard
blocked_reason: ""
baseline_commit: ""
---

# 中文指南批量生成与审校 - Workflow Run

> 工作流：zh-guide-workflow
> 任务：{task}
> 运行标识：{run_id}
> 创建时间：{date}
> 当前阶段：阶段 0
> 状态图例：⬜ 未开始 | 🔲 进行中 | ✅ 已完成 | ⏭️ 跳过

---

## 阶段 0：规划与枚举
- [ ] 已读路由文件与 .learnings/
- [ ] 已从 manifest 枚举缺失项（source != local 且 zh_guide=false）
- [ ] 已处理 desync（磁盘有标记但 manifest false 的 slug）
- [ ] 已与用户确认范围与严格度

### 目标清单
- [ ] {slug}

> [P0] ⬜ 未开始 {not_started}

---

## 阶段 1：同步与基线
- [ ] baseline_commit 已记录/验证
- [ ] .cache/upstream 已预热（sync-addons.py）
- [ ] 无 vendored 目录 dirty 阻塞

> [P1] ⬜ 未开始 {not_started}

---

## 阶段 2：批量生成
- [ ] 已按序生成全部目标的中文 README
- [ ] 已有 zh-guide 标记的未重写
- [ ] 每个 slug 复选框已勾选

> [P2] ⬜ 未开始 {not_started}

---

## 阶段 3：结构门禁
- [ ] zh-guide-gate.py --batch --strict 已跑
- [ ] 机械错误已就地修复
- [ ] 复验通过

> [P3] ⬜ 未开始 {not_started}

---

## 阶段 4：审校·修复·学习

### 批次结果表
| slug | source | 生成 | 门禁1 | 审校结论 | 修复项 | 门禁2 | 最终状态 |
|------|--------|------|-------|----------|--------|-------|----------|
| | | | | | | | |

> [P4] ⬜ 未开始 {not_started}

---

## 阶段 5：汇总与人工确认
- [ ] 已汇总 verdict 表
- [ ] 已交人工确认

> [P5] ⬜ 未开始 {not_started}

---

## 阶段 6：收尾发布
- [ ] manifest 已置 zh_guide:true
- [ ] --zh-status 已验证
- [ ] 已 commit 并 push origin + gitee

> [P6] ⬜ 未开始 {not_started}

---

## 异常记录

| 时间 | 阶段 | 问题描述 | 处理方式 |
|------|------|---------|---------|
| | | | |

---

## 最终产出

- **输出文件**：
- **完成状态**：
