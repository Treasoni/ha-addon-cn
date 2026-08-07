# 国内镜像源（registry proxy）与镜像地址重写规则

---
paths:
  - ".codex/scripts/registry_mirror.py"
  - ".codex/scripts/rewrite-images.py"
  - ".codex/scripts/check-images.py"
  - ".codex/scripts/sync-addons.py"
---

本仓库的 add-on `config.yaml` 里 `image:` 指向 `ghcr.io`，国内 HA 拉不到（TLS 被墙）。
本规则说明**如何验证可用镜像源**、**当前已知清单**、**如何改写与复验**。改写由脚本
完成，agent 不要手工编辑 config.yaml 的 image。

## 术语（与 CONTEXT.md 一致）

- **镜像源 / registry proxy**：pull-through 代理 `ghcr.io` 的国内镜像站（如 `ghcr.nju.edu.cn`）。
- **镜像地址重写（image rewrite）**：把 `image:` 行的 registry 主机换成镜像源的脚本化幂等变换。
- **post-sync transform**：同步管道里对 config.yaml 的重写步骤，保证改写不被下次同步冲掉。

## 如何验证一个镜像源是否可用

**唯一可靠方法**：打 manifest 端点 + config.yaml 的**真实 version**：

```bash
# 取真实 version（不要猜 latest）
GV=$(grep -m1 '^version:' grafana/config.yaml | awk '{print $2}')
curl -sS -o /dev/null -w "%{http_code}\n" -H "Accept: application/vnd.docker.distribution.manifest.list.v2+json, application/vnd.oci.image.index.v1+json" \
  "https://<镜像源>/v2/hassio-addons/grafana/amd64/manifests/$GV"
# 2xx = 可用；404 = 缺失；000 = 网络失败
```

**两个坑，勿踩**：
1. **勿用 `/v2/<repo>/tags/list`**——pull-through 代理对未缓存仓库返回假的 `NAME_UNKNOWN`。
2. **勿用 `latest` tag**——frenck / 官方镜像没有 `latest`，会假 404。必须用 `config.yaml`
   的 `version` 字段（Supervisor 实际拉的就是 `<image>:<version>`）。

脚本封装：`check-images.py`（全量校验）、`rewrite-images.py`（改写前探测选源）。

## 已知镜像源清单（2026-08-07 实测）

| 镜像源 | 代理 registry | 状态 | 说明 |
|---|---|---|---|
| `ghcr.nju.edu.cn` | ghcr.io | ✅ 可用 | 南京大学镜像站，免费匿名，pull-through 已验证 alexbelgium/frenck 全 200 |

新增候选流程：先用上面方法验证 → 追加到 `registry_mirror.py` 的 `KNOWN_MIRRORS` → 同步到本表。
**镜像源会死/限流**：不要以为一次验证永久有效。

## 复验节奏

- **每次同步**：`sync-addons.py` 同步开头调 `pick_sync_mirror()`，每 registry 打一次
  manifest（很便宜）；挂了自动回退 `KNOWN_MIRRORS[0]` 并告警。
- **全量校验**：`python .codex/scripts/check-images.py`（192 个逐个用真实 version 探测，
  可作发布门禁，ghcr 类失败退出码非 0）。

## 改写规则

- 只改 `config.yaml` 里 `image:` 行的 **registry 主机前缀**；保留行缩进、引号与
  `{arch}` 占位符形状（`-{arch}` 与 `/{arch}` 两种）。
- 主机属于 `{ghcr.io} ∪ KNOWN_MIRRORS` 才替换（支持换源迁移）；已是目标源则不变（幂等）。
- **`source: local` 的自有 add-on 永不触碰**（`rewrite-images.py` 与同步脚本均已内置保护）。
- **不碰 `build.json` 的 `build_from`**（那是本地构建的 base image，商店安装拉发布镜像，与重写无关）。
- **不改写 24 个官方 add-on**（image 是 Docker Hub 简写 `homeassistant/{arch}-addon-x`，
  实测 ghcr 镜像源 404，保持 Docker Hub 不动；国内用户请给 HA 配 Docker Hub 加速器）。

## 换源回退流程（镜像源挂了）

1. `python .codex/scripts/check-images.py` 确认哪个源失效。
2. 验证候选源（见上「如何验证」），追加进 `KNOWN_MIRRORS` 与本表。
3. `python .codex/scripts/rewrite-images.py`（自动探测选源，或 `--mirror` 指定）改完全部。
4. `python .codex/scripts/check-images.py` 复核全绿。
5. 提交并推送 origin + gitee（同步脚本下次会自动用新源继续改写）。

## 脚本入口

```bash
# 首次/换源批量改写（探测选源；--dry-run 预览；--mirror 指定）
python .codex/scripts/rewrite-images.py
# 全量可达性校验（发布门禁；--json 输出机器可读）
python .codex/scripts/check-images.py
# 同步（内含 pick_sync_mirror 探测 + post-sync transform）
python .codex/scripts/sync-addons.py
```
