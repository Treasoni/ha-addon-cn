# add-on 镜像国内化采用「同步后变换」（post-sync transform）而非原地改写

商店托管于 Gitee 后，中国用户仍无法安装 add-on：192 个 `config.yaml` 的 `image:` 指向 `ghcr.io`（国内 TLS 被墙）。要让商店真正「换成国内源」，必须把 `image:` 的 registry 主机改写为国内镜像源（如 `ghcr.nju.edu.cn`）。本 ADR 记录**改写如何在每次上游同步后存活**这一决策。

Status: accepted

**问题**：`sync-addons.py` 每次同步会把上游的 `config.yaml` 原样拷回（仅 README 豁免），且未提交的本地改动会让整个目录被同步跳过。原地手工改写一次，下次同步就被冲掉，还会阻塞上游更新。

**决策**：把镜像地址重写做成**同步管道里的幂等变换**——同步脚本拷入 config.yaml 时先过 `transform_yaml()`（`registry_mirror.py`）再落盘；对比时也先变换上游文本再与本地比较，因此无真实上游变更时不算 updated。`.cache/upstream/` 保持上游原样，商店目录里永远是改写版，每次同步自动重建，永不与同步打架。改写为幂等且支持换源迁移（主机 ∈ `{ghcr.io} ∪ KNOWN_MIRRORS` 才替换）。

**验证方法**（写进 `rules/common/mirror-sources.md`）：镜像源可用性必须用 manifest 端点 + config.yaml 真实 version 探测；`tags/list` 对未缓存仓库返回假 `NAME_UNKNOWN`，`latest` tag 对 frenck/官方不存在，两者都会误判。

**Considered Options**：
- 原地批量改写一遍——下次同步即被上游覆盖，且未提交期间阻塞同步，放弃。
- 独立「镜像分支/仓库」——main 保持上游原样、另生成改写版发布。最干净但需常驻生成步骤与双仓库维护，对本仓库规模过重，放弃。
- fork 成 `source: local`——完全脱离上游跟踪，192 个将失去更新来源，放弃。

**Consequences**：
- 商店目录的 `config.yaml` 与上游永久不一致（仅 `image:` 主机不同），未来维护者需知道这是有意为之——见 `CONTEXT.md`「镜像地址重写」与 `hassio-addon-sync` skill 禁止事项 #6 的例外说明。
- 每次同步自动复验镜像源（`pick_sync_mirror`），镜像源失效时可换源重跑 `rewrite-images.py` 整体迁移。
- 24 个官方 add-on 的镜像走 Docker Hub（`homeassistant/{arch}-addon-x` 简写），实测 ghcr 镜像源 404，不纳入重写，由国内用户配置 Docker Hub 加速器解决。
