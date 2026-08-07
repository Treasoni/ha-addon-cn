# 学习心得

---

_最后更新：2026-08-07_

- **`hassio.app_stdin` 是真实服务**（rpc_shutdown 审校）：HA 已将 add-on 改称 app，core 新增了 `hassio.app_stdin`（字段 `app`），与 `hassio.addon_stdin`（字段 `addon`）并存，均映射到 `/addons/{slug}/stdin`。上游官方 DOCS 已改用 `app_stdin`，中文 README 照抄不属于编造，切勿“纠正”成 addon_stdin。
- **官方源审校用本地镜像**：`.cache/upstream/official/{slug}/DOCS.md` 是官方完整文档，README 的端口/默认值/FAQ 声称均可直接对照，无需联网。
