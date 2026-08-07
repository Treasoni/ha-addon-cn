<!-- zh-guide -->
# Repository Updater

## 简介

Repository Updater（addons_updater）是一个面向 add-on 开发者的辅助工具，它通过比对上游新版本，自动更新 add-on 仓库中 `config.yaml` 的版本号与 `updater.json` 信息，并在有新版发布时自动提交更新。普通用户无需安装此加载项——Home Assistant 本身会自动提示 add-on 更新。仅当你在维护自己的 add-on 仓库时才需要它。

## 安装

1. 在 Home Assistant → 设置 → 加载项 → 商店，添加本商店仓库：
   - Gitee：https://gitee.com/zhqznc_10603234_123/ha-addon
   - GitHub：https://github.com/Treasoni/ha-addon-cn
2. 搜索 addons_updater 并安装。

## 配置

本加载项没有 Web 界面，配置分两部分完成：在 `addon_config` 中填写的加载项配置（用于连接仓库），以及仓库内 add-on 文件夹下的 `updater.json` 文件（用于描述每个 add-on 的上游来源）。加载项配置键如下：

| 配置键 | 类型 / 默认值 | 说明 |
| ------ | ----------- | ---- |
| `date_iso8601` | 布尔，默认 `true` | 使用 ISO8601 日期格式（YYYY-MM-DD）记录 `last_update`/`changelog` 条目，而不是 DD-MM-YYYY |
| `env_vars` | 列表，默认空 | 附加环境变量配置列表，每项由 `name` 与 `value` 组成，用于注入自定义脚本或运行环境 |
| `gitapi` | 字符串，默认 `gitapi` | 你的 GitHub API 令牌（classic），用于提交更新，在 https://github.com/settings/tokens 创建 |
| `gituser` | 字符串，默认 `gituser` | 你的 GitHub 用户名 |
| `repository` | 字符串，默认 `alexbelgium/hassio-addons` | 要更新的 add-on 仓库，格式为 `name/repo`（来自 GitHub） |
| `dry_run` | 可选布尔，默认空 | 试运行模式：测试更新但不会真正提交 |
| `gitmail` | 可选字符串，默认空 | 你的 GitHub 邮箱，用于提交记录 |
| `verbose` | 可选布尔，默认空 | 是否输出更详细的运行日志 |

> 补充说明：仓库内每个 add-on 文件夹下都需要一个 `updater.json` 文件，加载项只会更新包含该文件的 add-on。文件中可配置 `github_fulltag`、`github_beta`、`github_havingasset`、`github_tagfilter`、`github_exclude`、`paused`、`source`、`upstream_repo`、`dockerhub_by_date`、`dockerhub_list_size` 等标签，参见上游 README。

## 使用 / 访问入口

本加载项没有 Web 界面，属于后台开发者工具。安装并启动后，它会按计划自动比对上游发布，更新 add-on 版本号并提交；请通过加载项日志查看运行结果。

## 常见问题

- **普通用户需要安装它吗？** 不需要。这个工具面向 add-on 开发者。普通用户的 add-on 更新由 Home Assistant 自动提示。
- **为什么某些 add-on 没有被更新？** 只有在其仓库内包含 `updater.json` 文件的 add-on 才会被自动更新；此外可用 `paused: true` 暂停某个 add-on 的更新。
- **add-on 版本号为什么和上游标签不一样？** Home Assistant 无法排序 `version-bf9e0b4f` 或 `ubuntu-2026-06-01` 这类标签，加载项会保留原始上游标签在 `updater.json` 中，而在 `config.yaml` 里写 Home Assistant 可排序的版本号，避免同一发布重复触发更新。
- **更新失败怎么办？** 先确认 `gitapi` 令牌有效且具备提交权限、`repository` 与 `gituser` 填写正确，再查看日志定位具体错误。

---
- 英文原版：Home assistant add-on: addons updater；链接 https://github.com/alexbelgium/hassio-addons/blob/master/addons_updater/README.md
- 来源仓库：alexbelgium
