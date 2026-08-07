# 我的 Add-on 商店

面向国内用户的 Home Assistant Add-on 商店：把 GitHub 上主流 add-on **全量镜像**进本仓库（同时托管在 Gitee 与 GitHub），并附**中文使用指南**。也用于编写自己的 add-on。

- 仓库根目录即 HA Add-on 商店（`repository.json` + 各 add-on 目录）。
- 上游源：`alexbelgium/hassio-addons`（主源）· `home-assistant/addons`（官方）· `hassio-addons/repository`。
- 同步基线：`addons-manifest.json`；维护方式见下方「同步与维护」。

## 添加仓库

点击按钮一键添加（Home Assistant 需要能访问对应站点）：

[![添加到 Home Assistant（Gitee）](https://my.home-assistant.io/badges/store.svg)](https://my.home-assistant.io/redirect/store/?repository_url=https%3A%2F%2Fgitee.com%2Fzhqznc_10603234_123%2Fhomeassistant)
[![添加到 Home Assistant（GitHub）](https://my.home-assistant.io/badges/store.svg)](https://my.home-assistant.io/redirect/store/?repository_url=https%3A%2F%2Fgithub.com%2FTreasoni%2Fha-addon-cn)

或手动添加（设置 → 加载项 → 商店 → 右上角「…」→ 仓库）：

```
Gitee ：https://gitee.com/zhqznc_10603234_123/homeassistant   （国内推荐）
GitHub：https://github.com/Treasoni/ha-addon-cn
```

## Add-on 列表

- 完整清单见 `addons-manifest.json`（逐 add-on 标注来源、版本、中文指南状态）。
- 生成 Markdown 列表：`python .claude/scripts/sync-addons.py --readme-list`。
- 中文指南状态：`python .claude/scripts/sync-addons.py --zh-status`。

各 add-on 的 `README.md` 为**中文使用指南**（标记 `<!-- zh-guide -->`，由 skill 维护）。

## 同步与维护

上游仓库更新后，用 Claude Code skill 同步：

```
/sync-addons   （或触发词：同步 add-on、更新上游）
```

skill 会：浅克隆上游 → 比对复制变更 → 更新 manifest → 本地 commit → 推送 `origin`（GitHub）与 `gitee`（Gitee）两个远程。详见 `.claude/skills/hassio-addon-sync/SKILL.md`。

### 新建自有 add-on

```
python .claude/scripts/sync-addons.py --new-addon <slug> [--name "显示名"]
```

新 add-on 标记为 `source: local`，同步脚本永不触碰。完善 `config.yaml`、`Dockerfile`、`run.sh` 后，用 skill 生成中文 README。

## 许可证与署名

本商店仅为镜像聚合，各 add-on 版权归原作者所有：

| 来源 | 许可证 |
|---|---|
| [alexbelgium/hassio-addons](https://github.com/alexbelgium/hassio-addons) | MIT |
| [home-assistant/addons](https://github.com/home-assistant/addons) | Apache-2.0 |
| [hassio-addons/repository](https://github.com/hassio-addons/repository) | MIT |

自有 add-on 的版权归本仓库作者（zhq）所有。
