#!/usr/bin/env python3
"""
中文指南质量门禁（harness）。

确定性校验一份 Home Assistant add-on 的中文 README：
  - 结构检查（S1..S6）：文件存在、zh-guide 标记、必含标题、英文原版链接、无空单元格、无占位符；
  - 事实校验（F1..F6）：配置键反编造、options 覆盖、默认值一致、类型一致、端口真实、URL 合理。

同时提供 manifest 辅助：
  - --mark-zh <slug...>  将 addons-manifest.json 中对应 zh_guide 置为 true（先复验磁盘标记）；
  - --unmark-zh <slug...> 逆操作；
  - --dry-run 搭配 --mark-zh 只显示 diff。

无第三方依赖（不依赖 PyYAML，用轻量行级解析）。

退出码：0 = 通过（可含 WARN）；1 = 有 FAIL；2 = 用法/环境错误。
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

# Windows 控制台默认 GBK，强制 UTF-8 输出避免中文乱码
if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

ROOT = Path(__file__).resolve().parent.parent.parent
MANIFEST = ROOT / "addons-manifest.json"
ZH_MARKER = "<!-- zh-guide -->"

# 已核实：现有 45 篇中文指南共用这组标题
REQUIRED_HEADINGS = ["简介", "安装", "配置", "常见问题"]
ACCESS_HEADING_RE = re.compile(r"使用.*访问|访问入口|使用方法")

PLACEHOLDER_RE = re.compile(r"\bTODO\b|\bTBD\b|lorem|\bFIXME\b|待补充|占位")

STORE_URLS = (
    "github.com/Treasoni/ha-addon-cn",
    "gitee.com/zhqznc_10603234_123/homeassistant",
    "my.home-assistant.io",
)


# --------------------------------------------------------------------------- #
# 轻量 YAML 行级解析（不依赖 PyYAML）
# --------------------------------------------------------------------------- #
def _block_lines(text: str, field: str) -> list[tuple[int, str]]:
    """返回 `field:` 顶层键之后、下一个列 0 顶层键之前的 (行号, 行内容) 列表。"""
    lines = text.splitlines()
    start = None
    for i, ln in enumerate(lines):
        if re.match(rf"^{field}:\s*$", ln) or re.match(rf"^{field}:\s+\S", ln):
            start = i
            break
    if start is None:
        return []
    out = []
    for j in range(start + 1, len(lines)):
        ln = lines[j]
        stripped = ln.strip()
        if not stripped or stripped.startswith("#"):
            continue
        if not ln[:1].isspace():
            # 列 0 的下一顶层键（或文档结束）
            break
        out.append((j, ln))
    return out


def parse_yaml_keys(text: str, field: str) -> dict[str, str]:
    """
    提取 `field` 块（options/schema）下的扁平化键 → 值。
    只处理简单行结构；列表项与深层嵌套若无法稳定解析则跳过（交由审校 subagent 语义兜底）。
    """
    result: dict[str, str] = {}
    blocks = _block_lines(text, field)
    # 缩进基 = options/schema 块内第一级键的缩进（通常 2 空格）
    base_indent = None
    for _, ln in blocks:
        m = re.match(r"^(?P<indent>\s*)(?P<key>[A-Za-z0-9_]+):\s*(?P<value>.*)$", ln)
        if m:
            indent = len(m.group("indent"))
            if base_indent is None:
                base_indent = indent
            break
    if base_indent is None:
        return result

    stack: list[str] = []
    stack_indents: list[int] = []
    cur_indent = base_indent
    for _, ln in blocks:
        if ln.strip().startswith("-"):
            continue  # 列表项，非普通键
        m = re.match(r"^(?P<indent>\s*)(?P<key>[A-Za-z0-9_]+):\s*(?P<value>.*)$", ln)
        if not m:
            continue
        indent = len(m.group("indent"))
        key = m.group("key")
        value = m.group("value").strip()
        if not stack:
            stack.append(key)
            stack_indents.append(indent)
        elif indent > stack_indents[-1]:
            # 更深的缩进 = 子键
            stack.append(key)
            stack_indents.append(indent)
        else:
            # 同级或更浅 = 弹出到匹配缩进层再替换
            while stack_indents and indent < stack_indents[-1]:
                stack.pop()
                stack_indents.pop()
            if stack_indents and indent == stack_indents[-1]:
                stack[-1] = key
            else:
                # 跳级缩进（如父键之后直接回到 base 级），视为新顶层
                stack = [key]
                stack_indents = [indent]
        path = ".".join(stack)
        result[path] = value
    return result


def read_config(addon_dir: Path) -> dict:
    cfg = addon_dir / "config.yaml"
    if not cfg.is_file():
        return {}
    text = cfg.read_text(encoding="utf-8", errors="replace")
    parsed = {"text": text}
    m = re.search(r"^(?:name|version|slug|description|url|ingress|ingress_port):", text, re.MULTILINE)
    if m:
        parsed["raw"] = text
    parsed["options"] = parse_yaml_keys(text, "options")
    parsed["schema"] = parse_yaml_keys(text, "schema")
    # ports / ports_description
    ports = {}
    for _, ln in _block_lines(text, "ports"):
        mm = re.match(r"^\s*([\w\-\/\.]+):\s*([\d]+|null)\s*$", ln)
        if mm:
            ports[mm.group(1)] = mm.group(2)
    parsed["ports"] = ports
    parsed["ingress"] = bool(re.search(r"^ingress:\s*true\s*$", text, re.MULTILINE))
    parsed["ingress_port"] = ""
    return parsed


def flatten_option_keys(opt: dict[str, str]) -> set[str]:
    """options 顶层键集合（README 表格通常用扁平键，也兼容顶层）。"""
    tops = {k for k in opt if "." not in k}
    return tops


# --------------------------------------------------------------------------- #
# 单 add-on 门禁
# --------------------------------------------------------------------------- #
def check_addon(addon_dir: Path, strict: bool, manifest: dict | None) -> tuple[list[str], list[str]]:
    """
    返回 (issues, warns)。issue 形如 "[FAIL] S3 缺少标题：简介"；warn 形如 "[WARN] F2 ..."。
    """
    fails: list[str] = []
    warns: list[str] = []

    readme = addon_dir / "README.md"
    if not readme.is_file():
        return ["[FAIL] S1 缺少 README.md"], warns
    text = readme.read_text(encoding="utf-8", errors="replace")
    cfg = read_config(addon_dir)

    # ---- S1..S6 结构 ----
    # S2 标记
    marker_count = text.count(ZH_MARKER)
    if marker_count != 1:
        fails.append(f"[FAIL] S2 标记 {ZH_MARKER} 应恰好出现 1 次（实际 {marker_count}）")
    else:
        first = text.splitlines()[0:5]
        if not any(ZH_MARKER in ln for ln in first):
            fails.append("[FAIL] S2 标记应位于文件前 5 行内")

    # S3 必含标题
    headings = [ln.strip().lstrip("#").strip() for ln in text.splitlines() if re.match(r"^#{1,2} ", ln)]
    for h in REQUIRED_HEADINGS:
        if not any(h == head or head.startswith(h) for head in headings):
            fails.append(f"[FAIL] S3 缺少标题：{h}")
    if not any(ACCESS_HEADING_RE.search(h) for h in headings):
        fails.append("[FAIL] S3 缺少访问入口标题（使用/访问入口/使用方法）")

    # S4 文末英文原版（兼容纯文本与 markdown 链接两种既有风格）
    if not re.search(r"英文原版", text):
        fails.append("[FAIL] S4 缺少文末「英文原版」引用")
    elif not re.search(r"英文原版.*\[[^\]]+\]\(https?://[^)]+\)", text, re.MULTILINE | re.DOTALL):
        warns.append("[WARN] S4 英文原版为纯文本，建议附上游 raw URL 链接")

    # S5 表格空单元格
    table_rows = [ln for ln in text.splitlines() if re.match(r"^\s*\|.*\|\s*$", ln)]
    for ln in table_rows:
        cells = [c.strip() for c in ln.strip().strip("|").split("|")]
        if any(c == "" for c in cells) and not all(c == "" or set(c) <= {"-", ":"} for c in cells):
            fails.append(f"[FAIL] S5 配置表存在空单元格：{ln.strip()[:60]}")
            break

    # S6 占位符
    if PLACEHOLDER_RE.search(text):
        fails.append("[FAIL] S6 存在占位符（TODO/TBD/待补充/占位 等）")

    # ---- 配置表解析（事实校验前提）----
    table = parse_config_table(text)
    if cfg.get("options") or cfg.get("schema"):
        if not table:
            warns.append("[WARN] 未识别到配置表（需含「配置键」表头），跳过事实校验 F1–F4")

    # ---- F1..F4 事实 ----
    schema_keys = set(cfg.get("schema", {}).keys())
    option_keys = set(cfg.get("options", {}).keys())
    documented = set(table.keys()) if table else set()

    # F1 反编造：README 表键必须存在于 schema 或 options
    known = schema_keys | option_keys
    if table and known:
        for key in sorted(documented):
            # 兼容扁平键：任何 schema/options 键等于它或是它的前缀
            if not any(key == k or k.startswith(key + ".") or key.startswith(k + ".") for k in known):
                fails.append(f"[FAIL] F1 配置键 {key} 不在 config.yaml 的 schema/options 中")

    # F2 options 覆盖
    if option_keys and table:
        missing = [k for k in sorted(option_keys) if not any(k == d or d.startswith(k + ".") or k.startswith(d + ".") for d in documented)]
        if missing:
            msg = f"[FAIL] F2 未覆盖的 options 键：{', '.join(missing)}" if strict else f"[WARN] F2 未覆盖的 options 键：{', '.join(missing)}"
            (fails if strict else warns).append(msg)
    elif option_keys and not table:
        # options 非空但 README 未识别到配置表：按 schema 覆盖率报 WARN
        if schema_keys:
            covered = sum(1 for k in schema_keys if any(k == d or d.startswith(k + ".") for d in documented)) if documented else 0
            warns.append(f"[WARN] F2 README 无配置表，schema 覆盖率 {covered}/{len(schema_keys)}")

    # F3 默认值一致
    if option_keys and table:
        for key, val in sorted(cfg.get("options", {}).items()):
            if "." in key:
                continue  # 嵌套默认值交给审校 subagent
            if val in ("null", "", "[]"):
                continue
            row = table.get(key)
            if not row:
                continue
            readme_default = extract_default(row.get("type", ""))
            expected = normalize_value(val)
            if readme_default is not None and expected is not None and readme_default != expected:
                fails.append(f"[FAIL] F3 配置键 {key} 默认值不符：README={readme_default}，config.yaml={expected}")

    # F4 类型一致
    if cfg.get("schema") and table:
        for key, type_expr in sorted(cfg["schema"].items()):
            if "." in key:
                continue
            row = table.get(key)
            if not row:
                continue
            readme_type = row.get("type", "")
            type_token = schema_type_token(type_expr)
            readme_token = detect_readme_type(readme_type)
            if type_token and readme_token and not type_compatible(type_token, readme_token):
                fails.append(f"[FAIL] F4 配置键 {key} 类型不符：schema={type_expr}，README={readme_type[:40]}")

    # ---- F5 端口 ----
    check_ports(text, cfg, table, fails, warns)

    # ---- F6 URL ----
    check_urls(text, fails, warns)

    return fails, warns


def parse_config_table(text: str) -> dict[str, dict]:
    """解析 README 配置表 → {键: {"type": 类型/默认值单元格, "desc": 说明}}。"""
    lines = text.splitlines()
    result: dict[str, dict] = {}
    in_table = False
    header_idx = None
    for i, ln in enumerate(lines):
        if re.match(r"^\s*\|", ln) and "配置键" in ln:
            header_idx = i
            in_table = True
            break
    if header_idx is None:
        return result
    for j in range(header_idx + 1, len(lines)):
        ln = lines[j]
        if not re.match(r"^\s*\|", ln):
            break
        cells = [c.strip() for c in ln.strip().strip("|").split("|")]
        if len(cells) < 2:
            continue
        if all(set(c) <= {"-", ":"} for c in cells if c):
            continue  # 分隔行
        raw = cells[0].strip()
        # 键名可能是 `databases`（必填）——提取反引号内的完整键名
        m_key = re.match(r"^`([^`]+)`", raw)
        key = (m_key.group(1) if m_key else raw).strip()
        if not key or key == "配置键":
            continue
        result[key] = {"type": cells[1] if len(cells) > 1 else "", "desc": cells[2] if len(cells) > 2 else ""}
    return result


def extract_default(cell: str) -> str | None:
    """从「类型/默认值」单元格提取默认值。

    优先级（重要：先找「默认」后的值，再退回任意反引号值）：
    1. 中文布尔措辞（默认开启/关闭/启用/禁用/是/否）映射为 true/false；
    2. `默认 X` 后跟反引号包裹的完整值（如 `默认 `max-age=31536000; includeSubDomains``）——含空格也完整提取；
    3. `默认 X` 后跟无空格 token；
    4. 任意反引号包裹值（仅在无「默认」字样时使用，避免把类型 `str` 误当默认值）。
    """
    # 中文布尔措辞
    m = re.search(r"默认\s*(?:为\s*)?(开启|启用|是|关闭|禁用|否)", cell)
    if m:
        return "true" if m.group(1) in ("开启", "启用", "是") else "false"
    # `默认 X` 后的反引号包裹值（含空格也完整提取）
    m = re.search(r"默认(?:值)?\s*[：:]?\s*`([^`]+)`", cell)
    if m:
        return normalize_value(m.group(1))
    # `默认 X` 后跟无空格 token
    m = re.search(r"默认(?:值)?\s*[：:]\s*(?:`?)([^`，。\s,]+)", cell)
    if m:
        return normalize_value(m.group(1))
    # 无「默认」字样时退回任意反引号值
    if "默认" not in cell:
        m = re.search(r"`([^`]+)`", cell)
        if m:
            return normalize_value(m.group(1))
    return None


def normalize_value(v: str) -> str | None:
    v = v.strip().strip("`").strip().strip("'").strip('"')
    v = v.strip(",").strip()
    if v.lower() == "null" or v == "":
        return None
    return v


def schema_type_token(type_expr: str) -> str | None:
    m = re.match(r"^\s*(?P<base>list|int|str|bool|float|password|port)\b", type_expr)
    if m:
        base = m.group("base")
        if base == "list":
            return "list"
        return "list" if type_expr.strip().startswith("list(") else base
    m = re.match(r"^\s*match\(", type_expr)
    return "str" if m else None


def detect_readme_type(cell: str) -> str | None:
    for tok in ("布尔", "bool", "整数", "int", "字符串", "str", "密码", "password", "枚举", "list", "列表", "对象", "浮点", "float", "端口", "port"):
        if tok in cell:
            return {"布尔": "bool", "bool": "bool", "整数": "int", "int": "int",
                    "字符串": "str", "str": "str", "密码": "str", "password": "str",
                    "枚举": "str", "list": "list", "列表": "list", "对象": "list",
                    "浮点": "float", "float": "float", "端口": "int", "port": "int"}[tok]
    return None


def type_compatible(schema_tok: str, readme_tok: str) -> bool:
    if schema_tok == readme_tok:
        return True
    # list(...) 元素类型描述可接受
    if schema_tok == "list" and readme_tok in ("str", "bool", "int"):
        return True
    # HA schema 里 password 是字符串、port 是整数的语义别名
    if schema_tok == "password" and readme_tok == "str":
        return True
    if schema_tok == "port" and readme_tok == "int":
        return True
    return False


def check_ports(text: str, cfg: dict, table: dict, fails: list[str], warns: list[str]) -> None:
    known = set(cfg.get("ports", {}).keys())
    # 已知端口号 = 键中的数字（容器端口）+ 数字型宿主值；null 映射端口(如 8920/tcp: null)取键数字
    known_nums = set()
    for k in known:
        m = re.search(r"(\d{4,5})", k)
        if m:
            known_nums.add(m.group(1))
    for v in cfg.get("ports", {}).values():
        if v and str(v).isdigit():
            known_nums.add(str(v))
    if not known_nums:
        return
    # 配置表单元格里的端口是选项参数（如 WireGuard 隧道端口），不是 add-on 端口映射，不参与 F5
    table_nums = set()
    for row in table.values():
        for cell in (row.get("type", ""), row.get("desc", "")):
            for mm in re.findall(r"\d{4,5}", cell):
                table_nums.add(mm)
    # 正文端口提及分两类：
    #  - 明确端口语义（「端口 X」「映射到宿主端口 X」）→ 不匹配已知即 FAIL（编造端口）
    #  - `X/(udp|tcp)` 容器端口书写 → 不匹配已知仅 WARN（可能是外部服务，如 WireGuard 隧道）
    explicit = set()
    scheme = set()
    for m in re.finditer(r"端口[：:\s]*(\d{4,5})|(\d{4,5})/(udp|tcp)|映射到宿主[机]?\s*(?:端口)?\s*(\d{4,5})", text):
        g = m.group(1) or m.group(2) or m.group(3)
        if g and g.isdigit():
            if m.group(2):
                scheme.add(g)
            else:
                explicit.add(g)
    explicit -= table_nums  # 排除配置表里的配置值端口
    scheme -= table_nums
    fabricated = [p for p in sorted(explicit) if p not in known_nums]
    if fabricated:
        fails.append(f"[FAIL] F5 端口 {', '.join(fabricated)} 未出现在 config.yaml 的 ports 中")
    external = [p for p in sorted(scheme) if p not in known_nums]
    if external:
        warns.append(f"[WARN] F5 提及 `{', '.join(external)}/(udp|tcp)` 但 config.yaml 的 ports 未定义，可能是外部服务端口")
    mentioned = explicit | scheme
    if cfg.get("ingress"):
        if not re.search(r"ingress|侧边栏|打开 Web 界面|点击.*界面", text, re.IGNORECASE):
            warns.append("[WARN] F5 ingress=true 但 README 未提及 Ingress/侧边栏访问")
    elif known and not mentioned:
        warns.append("[WARN] F5 有端口定义但未能从 README 提取到任何端口号")


def check_urls(text: str, fails: list[str], warns: list[str]) -> None:
    urls = re.findall(r"https?://[^\s\)>]+", text)
    suspicious = False
    for u in urls:
        if re.search(r"\s|<|>", u):
            suspicious = True
            break
        host = re.match(r"https?://([^/]+)", u)
        if host and "." not in host.group(1):
            suspicious = True
            break
    if suspicious:
        warns.append("[WARN] F6 存在可疑 URL")
    if urls and not any(base in u for base in STORE_URLS for u in urls):
        warns.append("[WARN] F6 未找到商店安装链接（GitHub/Gitee/ha-addon）")


# --------------------------------------------------------------------------- #
# manifest 辅助
# --------------------------------------------------------------------------- #
def load_manifest() -> dict:
    if not MANIFEST.is_file():
        return {}
    return json.loads(MANIFEST.read_text(encoding="utf-8"))


def mark_zh(slugs: list[str], value: bool, dry_run: bool) -> int:
    manifest = load_manifest()
    if not manifest:
        print("错误：找不到 addons-manifest.json")
        return 2
    addons = manifest.setdefault("addons", {})
    changed = []
    for slug in slugs:
        entry = addons.get(slug)
        if entry is None:
            print(f"  [skip] {slug}：不在 manifest 中")
            continue
        addon_dir = ROOT / slug
        has_marker = (addon_dir / "README.md").is_file() and ZH_MARKER in (addon_dir / "README.md").read_text(encoding="utf-8", errors="replace")
        if value and not has_marker:
            print(f"  [skip] {slug}：磁盘 README 无 {ZH_MARKER} 标记，拒绝标记 zh_guide")
            continue
        if entry.get("zh_guide") == value:
            continue
        entry["zh_guide"] = value
        changed.append(slug)
    if dry_run:
        print(f"[dry-run] 将把 {len(changed)} 个 slug 的 zh_guide 置为 {value}: {', '.join(changed)}")
        return 0 if changed else 1
    if not changed:
        print(f"未修改任何 slug（全部跳过：不在 manifest / 无标记 / 已同值）。")
        return 1
    MANIFEST.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"已将 {len(changed)} 个 slug 的 zh_guide 置为 {value}: {', '.join(changed)}")
    return 0


# --------------------------------------------------------------------------- #
# CLI
# --------------------------------------------------------------------------- #
def main() -> int:
    parser = argparse.ArgumentParser(description="中文指南质量门禁")
    parser.add_argument("slug", nargs="?", help="单 add-on slug（仓库根目录下）")
    parser.add_argument("--batch", action="store_true", help="检查 manifest 中所有 zh_guide=false 的 add-on")
    parser.add_argument("--strict", action="store_true", help="F2 全覆盖转为 FAIL（否则 WARN）")
    parser.add_argument("--fixture", metavar="DIR", help="检查任意目录（测试用，无需 manifest）")
    parser.add_argument("--mark-zh", nargs="+", metavar="SLUG", help="把 zh_guide 置为 true（复验磁盘标记）")
    parser.add_argument("--unmark-zh", nargs="+", metavar="SLUG", help="把 zh_guide 置为 false")
    parser.add_argument("--dry-run", action="store_true", help="搭配 --mark-zh/--unmark-zh 只显示 diff")
    parser.add_argument("--json", action="store_true", help="按 slug 输出 JSON（机器解析）")
    args = parser.parse_args()

    if args.mark_zh:
        return mark_zh(args.mark_zh, True, args.dry_run)
    if args.unmark_zh:
        return mark_zh(args.unmark_zh, False, args.dry_run)

    if args.fixture:
        target = Path(args.fixture)
        if not target.is_dir():
            print(f"错误：目录不存在 {target}")
            return 2
        return run_gate(target, strict=args.strict, slug_label=target.name, as_json=args.json)

    if args.batch:
        manifest = load_manifest()
        if not manifest:
            print("错误：找不到 addons-manifest.json")
            return 2
        addons = manifest.get("addons", {})
        slugs = sorted(s for s, e in addons.items()
                       if e.get("source") != "local" and e.get("zh_guide") is False and (ROOT / s).is_dir())
        if not slugs:
            print("无待检查的缺失项")
            return 0
        return run_batch(slugs, strict=args.strict, as_json=args.json)

    if args.slug:
        target = ROOT / args.slug
        if not target.is_dir():
            print(f"错误：目录不存在 {target}")
            return 2
        return run_gate(target, strict=args.strict, slug_label=args.slug, as_json=args.json)

    parser.print_help()
    return 2


def run_gate(addon_dir: Path, strict: bool, slug_label: str, as_json: bool) -> int:
    manifest = load_manifest()
    fails, warns = check_addon(addon_dir, strict, manifest)
    if as_json:
        import json as _json
        print(_json.dumps({"slug": slug_label, "fail": fails, "warn": warns,
                           "passed": not fails}, ensure_ascii=False, indent=2))
    else:
        print(f"== {slug_label} ==")
        for line in fails + warns:
            print(f"  {line}")
        print(f"[{'PASS' if not fails else 'FAIL'}] {slug_label}")
    return 0 if not fails else 1


def run_batch(slugs: list[str], strict: bool, as_json: bool) -> int:
    results = []
    for slug in slugs:
        target = ROOT / slug
        fails, warns = check_addon(target, strict, load_manifest())
        results.append((slug, not fails, len(fails), warns))
    if as_json:
        import json as _json
        print(_json.dumps([{"slug": s, "passed": p, "fail_count": n, "warn": w}
                           for s, p, n, w in results], ensure_ascii=False, indent=2))
    else:
        passed = [s for s, p, _, _ in results if p]
        failed = [(s, n) for s, p, n, _ in results if not p]
        print(f"=== 中文指南门禁批次结果 ===")
        print(f"通过 ({len(passed)}): {', '.join(passed)}")
        if failed:
            print(f"失败 ({len(failed)}):")
            for s, n in failed:
                print(f"  - {s} ({n} 个 FAIL)")
    return 0 if all(p for _, p, _, _ in results) else 1


if __name__ == "__main__":
    sys.exit(main())
