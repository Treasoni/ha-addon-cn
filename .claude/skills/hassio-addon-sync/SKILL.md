---
name: hassio-addon-sync
description: 维护本仓库的 Home Assistant Add-on 商店：同步上游 add-on 变更、生成中文使用指南、从模板新建自有 add-on。触发词：同步 add-on、更新上游、add-on 商店、生成中文指南、新建 add-on、sync addons。
---

# Hassio Add-on 商店维护

本仓库根目录即一个 Home Assistant Add-on 商店（`repository.json` + 各 add-on 目录）。add-on 来自三个上游源**全量镜像**：

| 源 | 优先级 | 说明 |
|---|---|---|
| `alexbelgium/hassio-addons` | 1（主源） | MIT，~137 个 add-on |
| `home-assistant/addons` | 2 | 官方，Apache-2.0，~26 个 |
| `hassio-addons/repository` | 3 | frenck，MIT，~48 个 |

基线在 `addons-manifest.json`（提交入库）。同步脚本：`.claude/scripts/sync-addons.py`（无第三方依赖，`python` 直接跑）。

**镜像地址重写**：本商店面向国内用户，所有 vendored add-on 的 `config.yaml` `image:` 会由
同步脚本在每次同步时自动改写为国内镜像源（`ghcr.nju.edu.cn`，post-sync transform，幂等）。
规则与验证方法见 `.claude/rules/common/mirror-sources.md`；全量校验用
`python .claude/scripts/check-images.py`（发布前跑一次）。不要手工改 config.yaml 的 image。

## 触发场景

- **同步上游**：上游仓库更新了，本仓库要跟着更新。 → 走「同步流程」。
- **生成/更新中文指南**：某个 add-on 缺中文使用指南，或英文 README 变了想重翻。 → 走「中文指南流程」。
- **新建自有 add-on**：自己写一个 add-on。 → 走「脚手架流程」。
- **查看状态**：看 manifest、冲突、缺哪些中文指南。 → `python .claude/scripts/sync-addons.py --zh-status` / `--readme-list`。

## 同步流程

1. 运行同步脚本（会浅克隆/更新 `.cache/upstream/{源}`，目录已 gitignore）：
   ```
   python .claude/scripts/sync-addons.py
   ```
   想先看变更不动文件：加 `--dry-run`。
   脚本会自动：探测国内镜像源（每次复验一次）→ 把 vendored config.yaml 的 `image:`
   改写为镜像源（post-sync transform）→ 更新 manifest 的 `image_mirror`。
2. **审查变更摘要**：新增/更新/未变化/跳过/删除/冲突 各自数量与名单；`skipped` 里的 add-on 有未提交本地修改（含中文 README），不要覆盖。已改写的 add-on 应显示为「未变化」（幂等），若成片显示「更新」，先查 `git diff` 确认不是镜像重写误判。
3. **发布前跑镜像门禁**（确认所有 image 经镜像源可拉）：
   ```
   python .claude/scripts/check-images.py
   ```
   ghcr 类失败退出码非 0，别在有失败时推送。
4. 有变更则提交：
   ```
   git add -A
   git commit -m "sync: update add-ons from upstream (N updated, M added, K conflicts)"
   ```
5. **推送两个远程**（GitHub `origin` + Gitee `gitee`）：
   ```
   git push origin main
   git push gitee main
   ```
   认证失败（HTTPS/SSH 凭据）时不要反复重试，把命令与原因告诉用户，由用户手动推。
6. 若脚本输出「缺中文指南」清单，按需调用「中文指南流程」。

## 中文指南流程

目标：把 add-on 的 `README.md` 改写为中文（HA 详情页直接渲染 README.md）。`README.md` 是**本地维护文件**，同步脚本永不覆盖它。

对目标 slug（首批见 `guides/priority-list.md`，其余按需指定）：

1. 确认该 add-on 存在（本地目录或 `.cache/upstream/{源}/{slug}`）。
2. 阅读素材：`README.md`（上游英文原版，若已被中文版覆盖则看 `.cache` 里的原版）、`config.yaml`（选项与 schema）、`CHANGELOG.md`、必要时上游官方文档。
3. 用 `config.yaml` 里的 `name`、`description`、`options`/`schema` 核对事实，**翻译 + 本地化适配**，不编造。
4. 写入 `README.md`，结构建议：
   - 标题 + 一句用途（来自 config.yaml description）
   - 安装/添加仓库说明（Gitee/GitHub 地址）
   - 配置项说明（对应 options/schema，含默认值与单位）
   - 访问入口（ingress 或端口）
   - 常见问题
   - 文末「英文原版」链接到上游 README 的 raw URL，并注明来源仓库
   - 首部标记 `<!-- zh-guide -->`（脚本靠它识别中文指南）
5. 更新 manifest：
   ```
   python .claude/scripts/sync-addons.py --zh-status   # 确认该 slug 进入"已有"清单
   ```
   手工把 `addons-manifest.json` 里该 slug 的 `zh_guide` 置为 `true`（或同步脚本在检测到标记后由维护流程更新）。
6. 提交（同「同步流程」第 3~4 步）。

**禁止**：不编造配置项/端口/事实；上游 README 更新后想重翻，先跟用户确认（不要静默覆盖已有中文版）；一次只做几个，逐篇给用户审阅，不要一次性批量生成全部 200+ 篇未经审阅的指南。

## 脚手架流程（新建自有 add-on）

```
python .claude/scripts/sync-addons.py --new-addon <slug> [--name "显示名"] [--version 0.1.0]
```

- 从 `templates/new-addon/` 复制最小 run.sh 型模板，替换 slug/name/version，并在 manifest 注册为 `source: local`。
- **`source: local` 的 add-on 同步脚本永不触碰、永不删除**。
- 后续完善 `config.yaml` 的 `options`/`schema`、`Dockerfile`、`run.sh`、`icon.png`/`logo.png`，并按「中文指南流程」写中文 README。
- **完整开发走 `addon-authoring` skill / `addon-authoring-workflow`**（先收集上游资料 → 编写 → `check-addon.py` 门禁 → 审校 → 人工确认 → 发布）。本流程的快速脚手架只建目录，**发布前必须过 `python .claude/scripts/check-addon.py <slug>`**。

## 禁止事项

1. **永不修改 `source: local` 的自有 add-on**（同步脚本已内置保护，人工也不要去改）。
2. **永不覆盖本地已修改的 vendored add-on**（脚本会 `skipped` 并警告）。
3. **永不覆盖已有中文 README**（除非用户明确要求重翻）。
4. **不自动处理 Gitee/GitHub 凭据**；push 失败就如实报告。
5. **不 push 未审查的变更**——commit 前先看 `git status` 与脚本摘要。
6. **不手工修改上游 add-on 的内部文件内容**（只做整目录镜像与 README 本地化），除非是用户自有 add-on；**唯一例外**是脚本化的镜像地址重写（`sync-addons.py` 同步时自动对 config.yaml 的 `image:` 做 post-sync transform），agent 不要手工去改 image 字段。
