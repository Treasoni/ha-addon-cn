# 学习心得

---

_最后更新：2026-08-07_

- **`hassio.app_stdin` 是真实服务**（rpc_shutdown 审校）：HA 已将 add-on 改称 app，core 新增了 `hassio.app_stdin`（字段 `app`），与 `hassio.addon_stdin`（字段 `addon`）并存，均映射到 `/addons/{slug}/stdin`。上游官方 DOCS 已改用 `app_stdin`，中文 README 照抄不属于编造，切勿“纠正”成 addon_stdin。
- **官方源审校用本地镜像**：`.cache/upstream/official/{slug}/DOCS.md` 是官方完整文档，README 的端口/默认值/FAQ 声称均可直接对照，无需联网。

## 2026-08-07

### 镜像源（registry proxy）验证方法学

**类别**：knowledge_gap
**优先级**：high
**状态**：resolved（已落地 rules + registry_mirror.py）
**范围**：add-on 商店 / registry_mirror.py / mirror-sources.md

**摘要**：验证国内镜像源必须打 manifest 端点 + config.yaml 真实 version；`tags/list` 与 `latest` 都会给出假结果。

**详情**：
- 事实：`ghcr.io` 国内 TLS 被墙（curl schannel 握手失败）；`ghcr.nju.edu.cn` 对 alexbelgium/frenck 镜像的 manifest 端点返回 200，但对 `latest` 返回 404（frenck/官方没有 latest tag），对 `tags/list` 返回假 `NAME_UNKNOWN`（pull-through 代理只认已缓存仓库）。
- 根因：pull-through 代理在被拉取时才回源；add-on 镜像的 tag 是版本号而非 latest。
- 下次做法：一律 `GET https://<镜像源>/v2/<repo>/manifests/<真实version>`，2xx 才算可用；勿用 `tags/list`、勿用 `latest`。已固化到 `.claude/rules/common/mirror-sources.md` 与 `registry_mirror.py`。

---

### 对同步会覆盖的文件做系统性改写 = 同步后变换（post-sync transform）

**类别**：workflow
**优先级**：high
**状态**：resolved（ADR-0002 已 accepted）
**范围**：sync-addons.py / ADR-0002

**摘要**：对「同步脚本会从上游覆盖的文件」做系统性改写，必须做成同步管道里的幂等变换（拷贝后立即改写、改写后再与本地对比），不能原地手工改一遍。

**详情**：
- 事实：`sync-addons.py` 每次同步覆盖 config.yaml（仅 README 豁免），未提交改动会让目录被同步跳过。原地改写 168 个 config.yaml 会被下次同步冲掉。
- 根因：改写版与上游原版不一致，同步语义是「以上游为准」。
- 下次做法：拷贝后立即套 transform；对比时先变换上游文本再与本地比较（无真实变更则不误报 updated）；`.cache/upstream/` 保持上游原样。已落地 `sync-addons.py` + `registry_mirror.py`，决策见 `docs/adr/0002`。

---

### 国内访问 GitHub 会抖动

**类别**：knowledge_gap
**优先级**：medium
**状态**：pending
**范围**：sync-addons.py（依赖 github.com）

**摘要**：同一会话内 github.com 可能 fetch 连不上、push 又成功；同步/克隆失败先怀疑网络而非脚本。

**详情**：
- 事实：dry-run fetch 报 `Failed to connect to github.com:443`，几分钟后 `git push origin` 又成功。
- 根因：国内到 GitHub 的网络不稳定。
- 下次做法：同步脚本报网络类错误时，重试或稍后再跑，不要立刻改脚本；能离线验证的（如 transform 幂等测试）尽量不依赖网络。

---

### git status 快照可能过时

**类别**：best_practice
**优先级**：low
**状态**：pending
**范围**：所有任务

**摘要**：会话开始注入的 git status 可能与实现时真实状态不符，操作/提交前自己跑 git status 确认。

**详情**：
- 事实：会话开始时快照显示 60+ README 改动 + untracked netbird-server/README.md，实际运行时工作区完全干净。
- 根因：快照是会话起点时刻的，之后可能有提交发生。
- 下次做法：任何「基于当前工作区」的决策（提交范围、dirty 判断）前，先 `git status --short` 自证。
