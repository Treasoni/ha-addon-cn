# 错误日志

---

_最后更新：2026-08-08_

## 2026-08-08

### 审校：haos-mirror-switcher（source: local）

- 错误 1：`probe_all` 用 `active|reg` 扁平键写 state.json，而 `build_target` 读 `st["active"]` 嵌套字典 → 探测结果全被忽略，apply 永不写镜像。根因：bash 里手工拼 JSON 键用了 `|`，与消费者的嵌套结构不一致。修复：python 把探测结果结构化为 `{"active": {...}, "probe_results": {...}}` 再合并。预防：state 写入的键结构必须与读取方一致；JSON 用 python 结构化输出，勿用 bash 字符串拼接。
- 错误 2：`build_target` 的 patch 只含非空 mirror，"active 置 null 即移除"未实现 → `recover_direct`（恢复直连）实际什么都不做。根因：jq 对象合并 `(. + $patch)` 只覆盖已有键，patch 缺该键时旧映射保留。修复：enabled 的 registry 一律写 `patch[reg] = cur.get(reg)`（null 交给 `with_entries(select(.value != null))` 删除）。预防：jq 合并若要表达"删除"，patch 里必须显式写 null，再过滤 null 条目。
- 错误 3：`_mutate_proxies` 直接写 `/lib/proxy_hosts.json`（镜像层）→ 容器重建（HA 重启/更新）后用户增删的 gh-proxy 全丢。修复：增删持久化到 `/data/state.json` 的 `proxy_override`/`proxy_removed`，内置清单只读。预防：用户可编辑数据必须放挂载卷（/data），绝不写镜像层 /lib。
- 错误 4：OTA board 用 `uname -m` 推断 → ova/树莓派等非 generic 板会下载错误的 `.raucb`。修复：`/os/info` 的 `data.board` 为准，uname 仅作 fallback。预防：HAOS 板型信息从 Supervisor `/os/info` 拿，勿从内核 arch 猜。
- 错误 5：HAOS 宿主路径写 `/usr/share/hassio`、`/mnt/data/addons_config`（那是 Docker 安装/HASS 约定）。修复：HAOS 上 supervisor 数据在 `/mnt/data/supervisor`，addon_config 宿主路径为 `/mnt/data/supervisor/addons_config/{slug}`。预防：HAOS 宿主路径一律以 `/mnt/data/supervisor` 为根。
- 错误 6：config.yaml 的 `enable_ghcr/enable_dockerio/enable_lscr` 被 run.sh 读进 `ENABLE_*` 但无人消费，`enabled` 状态被硬编码全 true。修复：`probe_all`/`build_target` 用 `ENABLE_*` 环境变量与 state 的 enabled 共同生效。预防：options 读到 env 后必须确认被动作函数消费，否则文档与行为脱节。

## 2026-08-07

### 脚本（sync-addons.py）：输出到管道时中文变 GBK，grep 匹配不上

**错误**：`sync-addons.py --dry-run` 输出重定向后，用 UTF-8 中文 pattern grep 摘要两次都得到空结果，误以为命令没输出；实际是控制台/管道编码不一致，命令本身正常执行。

**触发场景**：Windows 下把脚本 stdout 重定向到文件或管道，且脚本未做 UTF-8 重配置时。

**根因**：Python 在 Windows 对重定向 stdout 使用 ANSI 代码页（GBK/cp936）编码；`registry_mirror.py` 已做 `sys.stdout.reconfigure(encoding="utf-8")`，而 `sync-addons.py` 没有，两边编码不一致。

**修复**：
- 已给 `sync-addons.py` 补上 `sys.stdout.reconfigure(encoding="utf-8")`，与 registry_mirror.py 一致。

**预防措施**：
- 新写 CLI 脚本统一加 stdout UTF-8 reconfigure。
- 排查「命令无输出」时，先检查重定向文件的实际编码，再认定是没执行或没匹配。

## 2026-08-07

### check-docker.sh：exec 形式检查误报全部 CMD/ENTRYPOINT

**错误**：`CMD [ "/run.sh" ]`、`CMD ["node", ...]` 全部被误报为「shell 形式，应改 JSON 数组」。

**触发场景**：用 `grep -nE '^(CMD|ENTRYPOINT)[[:space:]]' file` 按 `ln:rest` 切分后，直接 `case "$rest" in \[*)` 判断。

**根因**：`IFS=:` 切分后 `rest` 是从行首开始的整行，仍含 `CMD`/`ENTRYPOINT` 关键字，永远匹配不上 `\[*`。

**修复**：
- 判断前先 `sed -E 's/^(CMD|ENTRYPOINT)[[:space:]]+//'` 剥掉指令关键字，再看剩余内容是否以 `[` 开头。

**预防措施**：
- 从 `grep -n` 输出切出的 `rest` 是行首原文；判断内容前先剥掉行首指令关键字。
