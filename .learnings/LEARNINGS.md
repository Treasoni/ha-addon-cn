# 学习心得

---

_最后更新：2026-08-08_

## 2026-08-08

### source: local add-on 本地构建有两条镜像前置通道，缺一不可

**类别**：knowledge_gap
**优先级**：high
**状态**：resolved（已落地 haos-mirror-switcher README 前置步骤）
**范围**：source: local add-on / Supervisor 本地构建

**摘要**：Supervisor 构建 `source: local` 插件要拉两类镜像——①先从 Docker Hub 拉构建器 CLI 镜像（`docker:*`，仓库 `library/docker`，走 docker.io 通道）；②再按 config.yaml 从 ghcr.io 拉 `{arch}-base`。只配 `registries_mirror` 的 ghcr.io 映射，构建会因拉不到 Docker Hub 的 `docker:...-cli` 而失败（`Can't pull image docker:29.6.2-cli` / `auth.docker.io ... EOF`）。

**详情**：
- 事实：真机装 `haos-mirror-switcher` 报 `Pulling image docker:29.6.2-cli` → `failed to authorize ... repository:library/docker:pull` → EOF。用户在 docker.json 只配了 ghcr.io 映射。
- 根因：构建 source: local 需要 Docker Hub 的 `library/docker` CLI 镜像作为构建器，这是 docker.io 通道；它不在 ghcr.io 映射覆盖范围内。
- 下次做法：source: local 插件的「手动换源前置」必须**同时**配好 `{ "ghcr.io": ..., "docker.io": ... }` 两个映射，README 前置步骤要写明这条硬依赖。已在 haos-mirror-switcher README 补齐。

### 预构建镜像发布三条铁律（build-addon.yml + GHCR）

**类别**：knowledge_gap
**优先级**：high
**状态**：resolved（已落地 build-addon.yml / config.yaml / ADR-0004）
**范围**：source: local 预构建 add-on / GitHub Actions buildx 推送 ghcr.io

**摘要**：haos-mirror-switcher 转预构建模式，首轮 CI 构建连挂三轮，三条根因分别是被 buildx/docker 强制的规范：

**详情**：
- ① image tag 必须带完整 registry 前缀：`ghcr.io/<owner>/<slug>-{arch}`，只写 `<owner>/<slug>-{arch}` 会把 owner 当主机名，报 `failed to push Treasoni/...: lookup Treasoni: no such host`。workflow 里用 `IMAGE_REGISTRY` env 拼全。
- ② Docker 镜像仓库名（namespace/repo 部分）必须**全小写**：`Treasoni/...` 直接报 `invalid tag ... repository name must be lowercase`。config.yaml `image:` 与 workflow tags 同步改 `ghcr.io/treasoni/...`（GitHub 用户名大小写不敏感，登录/推送不受影响）。
- ③ GHCR 容器包**默认 private**，匿名 pull 403（镜像在、但 HA/镜像源拉不到）；且**个人账号包的可见性无法用 REST API 改**（`/user/packages/.../visibility` 返回 404，该端点只有 org 版），必须 web UI：包页面 → ⚙ Package settings → Danger Zone → Change visibility → Public。gh token 需 `read:packages,write:packages` scope 才能查包。

---

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

---

### bash 条件判断：`[[ ==/!= ]]` 右值是 glob，不是 regex

**类别**：knowledge_gap
**优先级**：high
**状态**：resolved（已固化到 check-docker.sh 与 RULES.md）
**范围**：check-docker.sh / bash 脚本

**摘要**：`[[ "$x" != *pat* ]]` 里 `+` 是字面量、`[[:space:]]` 只匹配单字符，不能当正则用；regex 必须用 `=~`，否定用 `! [[ "$x" =~ pat ]]`。

**详情**：
- 事实：用 `[[ "$block" != *rm[[:space:]]+-rf[[:space:]]+/var/lib/apt/lists* ]]` 判断多行 RUN 是否清理 apt 缓存，`rm -rf` 明明在却误报「未清理」。
- 根因：`[[ ==/!= ]]` 右值是 glob pattern，`+` 是字面量；我把 glob 与 regex 语义混用了。
- 下次做法：字符串包含判断用 `[[ "$s" =~ pat ]]`；否定用 `! [[ "$s" =~ pat ]]`；要 `+`/`[[:space:]]+` 量词时必须走 `=~`。

---

### Dockerfile 校验的解析边界（check-docker.sh）

**类别**：knowledge_gap
**优先级**：high
**状态**：resolved（已固化到 .claude/scripts/check-docker.sh）
**范围**：.claude/scripts/check-docker.sh

**摘要**：写 Dockerfile 检查器不能假设 `FROM <img>` 简单形态：有 `FROM --platform=$X <img>`、`FROM <stage>`（多阶段别名）、`ARG BUILD_FROM=默认值`、官方镜像名用连字符等边界。

**详情**：
- 事实：`FROM --platform=$BUILDPLATFORM golang:1.26-trixie AS buildenv` 被当裸仓库名；`FROM buildenv AS build` 的别名被当裸仓库；`ARG BUILD_FROM=ghcr.io/...` 没被识别为 add-on（被分类成 generic）；官方 `homeassistant/{arch}-addon-matter-server` 因连字符没过 `[A-Za-z0-9_]+` 正则。
- 根因：FROM 的镜像 ref 不一定是第一个 token（`--flag` 在前）；addon 判定忽略了带默认值的 `ARG`；镜像名允许 `-`。
- 下次做法：FROM 解析先跳过 `--flag` token；先收集全部 `AS <name>` 放行别名；addon 判定用 `^ARG BUILD_FROM([[:space:]]|=|$)`；镜像名字符集含 `-`。

---

### 校验 Dockerfile 必须按逻辑 RUN 语句判断

**类别**：best_practice
**优先级**：medium
**状态**：resolved
**范围**：.claude/scripts/check-docker.sh

**摘要**：`RUN apt-get update \ && ... \ && rm -rf /var/lib/apt/lists/*` 是跨多物理行的单个 RUN，按物理行检查会误报；先把 `\` 续行合并成逻辑语句再判断。

**详情**：
- 事实：Dockerfile.generic 里 4 行续行 RUN 被报「apt-get update 未清理缓存」，但同一语句第 3 行有 `rm -rf /var/lib/apt/lists/*`。
- 根因：docker 构建单元是逻辑语句（`\` 续行），不是物理行。
- 下次做法：用 awk 把以 `\` 结尾的续行合并为逻辑 RUN（输出起始行 + 全文），再对整块判断 flag/清理；不要逐物理行 grep。
