---
workflow_id: addon-authoring-workflow
workflow_name: 自有 add-on 开发
workflow_version: 1
state_file_type: workflow-run
run_id: "{run_id}"
task: "{task}"
created_from: ".claude/workflows/addon-authoring-workflow/state-template.md"
created_at: "{date}"
last_updated: "{date}"
current_phase: P0
current_status: not_started
mode: standard
blocked_reason: ""
baseline_commit: ""
---

# 自有 add-on 开发 - Workflow Run

> 工作流：addon-authoring-workflow
> 任务：{task}
> 运行标识：{run_id}
> 创建时间：{date}
> 当前阶段：阶段 0
> 状态图例：⬜ 未开始 | 🔲 进行中 | ✅ 已完成 | ⏭️ 跳过

---

## 阶段 0：规划与确认
- [ ] 已读路由文件与 .learnings/
- [ ] 已与用户确认 slug / name / version / 上游软件 URL
- [ ] 已从 state-template.md 创建状态文件
- [ ] 已确认 build.json 会由脚手架生成

> [P0] ⬜ 未开始 {not_started}

---

## 阶段 1：脚手架与资料收集
- [ ] sync-addons.py --new-addon <slug> 已运行建目录
- [ ] 上游官方资料已收集（功能/端口/账号/数据目录/env/版本）
- [ ] config.yaml 头部「上游资料卡」注释块已填写
- [ ] config.yaml 无 image 字段、build.json 已生成

> [P1] ⬜ 未开始 {not_started}

---

## 阶段 2：编写实现
- [ ] config.yaml 已按资料卡编写（url/description/options/schema 一一对应）
- [ ] Dockerfile/run.sh 与 config 一致（bashio::config 引用键存在于 options）
- [ ] 中文 README 已编写（首行 zh-guide 标记，含简介/安装/配置/使用/常见问题）

> [P2] ⬜ 未开始 {not_started}

---

## 阶段 3：结构门禁
- [ ] check-addon.py <slug> 已跑
- [ ] 机械错误已就地修复
- [ ] 复验通过（或已 block 并记录异常）

> [P3] ⬜ 未开始 {not_started}

---

## 阶段 4：审校复验

### 审校结果
| 检查项 | 结论 | 修复项 |
|--------|------|--------|
| options/schema 与资料卡及上游一致 | | |
| description / url 真实 | | |
| build.json 覆盖 arch | | |
| run.sh 键存在 / README 与 config 一致 | | |

> [P4] ⬜ 未开始 {not_started}

---

## 阶段 5：汇总与人工确认
- [ ] 已汇总 verdict 表（通过 / 修复后通过 / 失败）
- [ ] 已交用户人工确认

> [P5] ⬜ 未开始 {not_started}

---

## 阶段 6：收尾发布
- [ ] manifest 已复验 source==local 且 local_version 正确
- [ ] 已 commit 并 push origin + gitee
- [ ] 认证失败时已报告用户、不重试

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
