# 错误日志

---

_最后更新：2026-08-07_

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
