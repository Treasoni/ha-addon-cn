# 我的 Add-on 商店

一个**面向国内用户**的 Home Assistant Add-on 商店：把 GitHub 上主流 add-on **全量镜像**到 Gitee，安装不再被网络卡住；主流 add-on 还附**中文使用指南**。

- 📦 **192 个 add-on**：来自 alexbelgium（130）、Home Assistant 官方（24）、frenck 社区（38）三大源，与上游保持同步。
- 🇨🇳 **国内可用**：主仓库托管在 Gitee，不用科学上网也能添加、安装、更新。
- 📖 **中文指南**：45 个主流 add-on 已提供中文使用指南（HA 详情页直接显示中文）。

---

## 快速开始（3 步）

1. **添加仓库**（见下）
2. **安装 add-on**：商店里搜索名字 → 安装 → 启动
3. **看中文指南**：进入 add-on 详情页 → 「README / 文档」标签即中文说明

---

## 第一步：添加仓库

### 方式一：一键添加（推荐）

点击按钮会打开 Home Assistant 并自动添加本商店（需要已登录你的 HA）：

[![添加到 Home Assistant（Gitee，国内推荐）](https://my.home-assistant.io/badges/store.svg)](https://my.home-assistant.io/redirect/store/?repository_url=https%3A%2F%2Fgitee.com%2Fzhqznc_10603234_123%2Fha-addon)
[![添加到 Home Assistant（GitHub 备用）](https://my.home-assistant.io/badges/store.svg)](https://my.home-assistant.io/redirect/store/?repository_url=https%3A%2F%2Fgithub.com%2FTreasoni%2Fha-addon-cn)

### 方式二：手动添加

1. 进入 Home Assistant → **设置 → 加载项 → 商店**
2. 点右上角 **「…」→ 仓库**
3. 粘贴仓库地址 → **添加**：
   - **Gitee（国内推荐）**：`https://gitee.com/zhqznc_10603234_123/ha-addon`
   - GitHub 备用：`https://github.com/Treasoni/ha-addon-cn`
4. 回到商店页面，稍等片刻即可看到「我的 Add-on 商店」及其 add-on 列表。

> 💡 **为什么选 Gitee？** Gitee 在国内访问快且稳定；GitHub 仅在你能正常访问时作为备用。

---

## 第二步：安装 add-on

1. 在商店搜索框输入名字（如 `jellyfin`、`bazarr`、`samba`、`ssh`、`node-red`）。
2. 点击进入详情页，阅读**中文使用指南**，确认配置项。
3. 点 **安装**，等待构建完成（首次安装可能需要几分钟）。
4. 在「配置 / 网络 / 权限」里按需开启端口映射、设备（如 `/dev/dri` 硬解）、权限后保存。
5. 点 **启动**。

> ⚠️ 某些 add-on 需要额外权限或设备（如硬件加速、USB 设备），安装后先在详情页的「权限」「设备」标签里勾选，否则可能无法正常访问硬件。

---

## 第三步：使用中文指南

- 每个 add-on 的 `README.md` 都是**中文使用指南**，包含：简介、安装、配置项表格、访问入口、常见问题。
- 查看方式：add-on 详情页 → **「README」/「文档」标签**（HA 渲染该 add-on 的 README.md）。
- 目前 **45/192** 个 add-on 有中文指南（主流媒体、家庭服务、官方基础设施、自动化网络类已覆盖）。缺中文指南的 add-on 仍显示上游英文说明，会陆续补齐。
- 想确认哪个有中文指南：本仓库根目录 `addons-manifest.json` 里每个 add-on 的 `zh_guide` 字段；或直接打开仓库里对应 add-on 文件夹看 README.md 是否以 `<!-- zh-guide -->` 开头。

---

## 更新 add-on

- **add-on 版本更新**：HA 会在商店里提示「有可用更新」，直接点更新即可（与官方/上游节奏一致）。
- **本商店内容更新**：上游仓库更新后，本商店会定期同步（维护者用 Claude Code skill `hassio-addon-sync` 执行，详见仓库 `.claude/skills/`）。你无需手动刷新，HA 会自动拉取新版本。

---

## 常见问题（FAQ）

**Q：添加后商店里看不到任何 add-on？**
- 确认仓库地址无误；HA 加载新仓库后可能需等待几秒，点商店页面刷新。仍不行就重新添加一次。
- 确认你的 HA 能访问 Gitee（国内网络一般没问题）。

**Q：搜不到某个 add-on？**
- 先确认它在本商店（查看本仓库的 add-on 文件夹清单）。同名 add-on 在不同仓库可能存在，搜索时认准「我的 Add-on 商店」来源。

**Q：add-on 安装很慢 / 卡在下载？**
- 首次安装需要拉取容器镜像，取决于网络与机型；`aarch64`（树莓派等）比 `amd64` 慢。建议国内用户连接 Docker 镜像加速。

**Q：为什么有的 add-on 只有英文说明？**
- 中文指南在陆续补齐中（当前 45/192）。优先覆盖了主流 add-on；其余可按需在仓库里提需求。

**Q：这个商店和官方商店冲突吗？**
- 不冲突。本商店是第三方社区商店，与 Home Assistant 官方 add-on 商店并行；同名 add-on（如 `samba`、`ssh`）以本商店为准或任选其一安装。

---

## 这个商店是什么

- **全量镜像**：三个上游源的所有 add-on 目录原样复制到本仓库，保持与上游一致：
  - [alexbelgium/hassio-addons](https://github.com/alexbelgium/hassio-addons)（MIT）— 130 个
  - [home-assistant/addons](https://github.com/home-assistant/addons)（Apache-2.0）— 24 个（官方）
  - [hassio-addons/repository](https://github.com/hassio-addons/repository)（MIT）— 38 个
  - 同名 add-on 按 alexbelgium > 官方 > frenck 优先级取一份。
- **同步基线**：`addons-manifest.json`（每个 add-on 的来源、版本、中文指南状态都在里面）。

---

## 许可证与署名

本商店仅为镜像聚合，各 add-on 版权归原作者所有（来源与许可证见上表）；自有 add-on 的版权归本仓库作者（zhq）所有。

---

## 维护者专用

- 同步上游：`python .claude/scripts/sync-addons.py`（或 Claude Code skill `hassio-addon-sync`）
- 中文指南：skill `zh-guide-workflow`（批量生成 / 审校）
- 新建自有 add-on：`python .claude/scripts/sync-addons.py --new-addon <slug>`
