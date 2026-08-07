#!/usr/bin/env python3
"""
自有 add-on 编写门禁（harness）。

按 addon-authoring 规范附录 B 验收标准，确定性校验一个 `source: local`
自有 add-on：目录/manifest、config.yaml 结构、上游资料卡、description/version、
arch 合法性、options/schema 一致性、schema 类型合法性、禁止 image 字段、
build.json 覆盖。

检查项 C1..C10（FAIL）+ 提示项 W1/W2（WARN）。

无第三方依赖（不依赖 PyYAML，用轻量行级解析，风格同 zh-guide-gate.py）。

用法：
  check-addon.py <slug>            # 校验 ROOT/<slug>（要求 manifest source=local）
  check-addon.py --all             # 校验 manifest 中所有 source=local 的 add-on
  check-addon.py --fixture DIR     # 校验任意目录（测试用，无 manifest 检查）
  check-addon.py --json            # 机器可读 JSON 输出

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

REQUIRED_FIELDS = ["name", "version", "slug", "description", "url", "arch", "startup", "boot"]
ARCH_PLATFORMS = {"aarch64", "amd64", "armv7", "armhf", "i386"}
SCHEMA_BASE_TYPES = {"str", "int", "bool", "float", "port", "password", "list", "dict"}
DESC_PLACEHOLDER_RE = re.compile(r"(在这里写|待补充|TODO|TBD|FIXME|lorem|占位)", re.IGNORECASE)
INFO_CARD_MARKER = "上游资料卡"


# --------------------------------------------------------------------------- #
# 轻量 YAML 行级解析（不依赖 PyYAML）
# --------------------------------------------------------------------------- #
def _block_lines(text: str, field: str) -> list[tuple[int, str]]:
    """返回 `field:` 顶层键之后、下一个列 0 顶层键之前的 (行号, 行内容) 列表。

    兼容列表项在列 0 与缩进两种风格：列 0 的列表项（`- x`）属于块内，不中断。
    """
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
        if not ln[:1].isspace() and not stripped.startswith("-"):
            # 列 0 的下一顶层键（或文档结束）
            break
        out.append((j, ln))
    return out


def _block_top_keys(text: str, field: str) -> list[str]:
    """返回 `field` 块（options/schema）内第一缩进层级的键列表（忽略列表项与嵌套）。"""
    blocks = _block_lines(text, field)
    base_indent = None
    for _, ln in blocks:
        m = re.match(r"^(?P<indent>\s*)(?P<key>[A-Za-z0-9_]+):\s*", ln)
        if m:
            base_indent = len(m.group("indent"))
            break
    if base_indent is None:
        return []
    keys = []
    for _, ln in blocks:
        if ln.strip().startswith("-"):
            continue
        m = re.match(r"^(?P<indent>\s*)(?P<key>[A-Za-z0-9_]+):\s*(?P<value>.*)$", ln)
        if m and len(m.group("indent")) == base_indent:
            keys.append(m.group("key"))
    return keys


def _block_top_values(text: str, field: str) -> dict[str, str]:
    """返回 `field` 块第一缩进层级的 键 → 值（去行内注释）。"""
    blocks = _block_lines(text, field)
    base_indent = None
    for _, ln in blocks:
        m = re.match(r"^(?P<indent>\s*)(?P<key>[A-Za-z0-9_]+):\s*", ln)
        if m:
            base_indent = len(m.group("indent"))
            break
    if base_indent is None:
        return {}
    result: dict[str, str] = {}
    for _, ln in blocks:
        if ln.strip().startswith("-"):
            continue
        m = re.match(r"^(?P<indent>\s*)(?P<key>[A-Za-z0-9_]+):\s*(?P<value>.*)$", ln)
        if m and len(m.group("indent")) == base_indent:
            value = m.group("value").strip()
            value = re.sub(r"\s+#.*$", "", value).strip()  # 去行内注释
            result[m.group("key")] = value
    return result


def _arch_values(text: str) -> list[str]:
    """返回 arch 块下的架构列表。兼容列 0 与缩进两种列表风格及内联 `[a, b]`。"""
    lines = text.splitlines()
    start = None
    for i, ln in enumerate(lines):
        if re.match(r"^arch:", ln):
            start = i
            break
    if start is None:
        return []
    line0 = lines[start].strip()
    m_inline = re.match(r"^arch:\s*\[(.*)\]", line0)  # 允许行内 [a, b] 及尾部注释
    if m_inline:
        body = re.sub(r"\s+#.*$", "", m_inline.group(1)).strip()
        return [x.strip().strip('"').strip("'") for x in body.split(",") if x.strip()]
    out = []
    for ln in lines[start + 1:]:
        stripped = ln.strip()
        if not stripped or stripped.startswith("#"):
            continue
        if not ln[:1].isspace() and not stripped.startswith("-"):
            break
        m = re.match(r"^-\s*(.+)$", stripped)
        if m and m.group(1).strip():
            item = re.sub(r"\s+#.*$", "", m.group(1)).strip()  # 去行内注释
            if item:
                out.append(item)
    return out


def _info_card_lines(text: str) -> list[str]:
    """返回 `# === 上游资料卡 ===` 起始的注释块行（含空行），找不到返回 []。"""
    lines = text.splitlines()
    for i, ln in enumerate(lines):
        if ln.strip().startswith("#") and INFO_CARD_MARKER in ln:
            out = [ln]
            for j in range(i + 1, len(lines)):
                s = lines[j].strip()
                if not s:
                    continue
                if not s.startswith("#"):
                    break
                out.append(lines[j])
            return out
    return []


# --------------------------------------------------------------------------- #
# schema 类型合法性
# --------------------------------------------------------------------------- #
def _split_top_level(value: str) -> list[str]:
    """在圆/花/方括号深度 0 处按 `|` 切分（`match(^a|b$)`、`list(a|b)` 不切）。"""
    parts: list[str] = []
    depth = 0
    cur: list[str] = []
    opens = {"(", "{", "["}
    closes = {")", "}", "]"}
    for ch in value:
        if ch in opens:
            depth += 1
        elif ch in closes:
            depth -= 1
        if ch == "|" and depth == 0:
            parts.append("".join(cur))
            cur = []
        else:
            cur.append(ch)
    parts.append("".join(cur))
    return parts


def _brackets_balanced(s: str) -> bool:
    stack: list[str] = []
    pairs = {")": "(", "}": "{", "]": "["}
    for ch in s:
        if ch in "({[":
            stack.append(ch)
        elif ch in pairs:
            if not stack or stack.pop() != pairs[ch]:
                return False
    return not stack


def _valid_schema_type(value: str) -> bool:
    """校验单个 schema 值：基础类型 | match(..) | list(..) | {...}，支持 | 联合与每个成员尾部 ?。

    YAML 引号（"str" / 'str'）与裸 str 语义等同，先剥离；`int?|str` 这类逐成员可选也接受。
    """
    v = value.strip()
    if not v:
        return False
    # 剥离 YAML 标量引号
    if len(v) >= 2 and v[0] == v[-1] and v[0] in "\"'":
        v = v[1:-1].strip()
    if not v:
        return False
    for p in _split_top_level(v):
        p = p.strip()
        if not p:
            return False
        if p.endswith("?"):
            p = p[:-1].rstrip()  # 逐成员可选后缀
        if not p:
            return False
        if p in SCHEMA_BASE_TYPES:
            continue
        if p.startswith("match(") and p.endswith(")") and _brackets_balanced(p):
            continue
        if p.startswith("list(") and p.endswith(")") and _brackets_balanced(p):
            continue
        if p.startswith("{") and p.endswith("}") and _brackets_balanced(p):
            continue
        return False
    return True


# --------------------------------------------------------------------------- #
# 单 add-on 门禁
# --------------------------------------------------------------------------- #
def check_addon(addon_dir: Path, is_fixture: bool, source: str | None) -> tuple[list[str], list[str]]:
    """返回 (fails, warns)。fails 形如 "[FAIL] C3 缺少必填字段：name"；warns 形如 "[WARN] W1 ..."。"""
    fails: list[str] = []
    warns: list[str] = []

    # C1 addon 目录存在；(非 fixture) manifest source == local
    if not addon_dir.is_dir():
        fails.append("[FAIL] C1 addon 目录不存在")
        return fails, warns
    if not is_fixture:
        if source is None:
            fails.append("[FAIL] C1 manifest 未注册该 slug")
        elif source != "local":
            fails.append(f"[FAIL] C1 manifest 中 {addon_dir.name} 的 source={source}，应为 local")

    # C2 config.yaml 存在且非空
    cfg_path = addon_dir / "config.yaml"
    if not cfg_path.is_file():
        fails.append("[FAIL] C2 缺少 config.yaml")
        return fails, warns
    text = cfg_path.read_text(encoding="utf-8", errors="replace")
    if not text.strip():
        fails.append("[FAIL] C2 config.yaml 为空")
        return fails, warns

    # C3 必填字段（顶层键）
    missing = [f for f in REQUIRED_FIELDS if not re.search(rf"^{f}:", text, re.MULTILINE)]
    if missing:
        fails.append(f"[FAIL] C3 缺少必填字段：{', '.join(missing)}")

    # C4 头部（前 20 行内）上游资料卡注释块
    head_lines = text.splitlines()[:20]
    if not any(ln.strip().startswith("#") and INFO_CARD_MARKER in ln for ln in head_lines):
        fails.append("[FAIL] C4 config.yaml 前 20 行内缺少「# === 上游资料卡 ===」注释块")

    # C5 description 非空、非占位符
    m = re.search(r"^description:\s*(.*)$", text, re.MULTILINE)
    if not m:
        fails.append("[FAIL] C5 缺少 description")
    else:
        desc = m.group(1).strip().strip('"').strip("'").strip()
        if not desc:
            fails.append("[FAIL] C5 description 为空")
        elif DESC_PLACEHOLDER_RE.search(desc):
            fails.append(f"[FAIL] C5 description 含占位符：{desc[:40]}")

    # C6 version 引号包裹且非空
    m = re.search(r"^version:\s*(.*)$", text, re.MULTILINE)
    if not m:
        fails.append("[FAIL] C6 缺少 version")
    else:
        raw = m.group(1).strip()
        q = re.match(r'^"([^"]*)"\s*$', raw) or re.match(r"^'([^']*)'\s*$", raw)
        if not q:
            fails.append(f"[FAIL] C6 version 需用引号包裹：{raw[:40]}")
        elif not q.group(1).strip():
            fails.append("[FAIL] C6 version 引号内为空")

    # C7 arch 非空且 ∈ 合法平台
    arch = _arch_values(text)
    if not arch:
        fails.append("[FAIL] C7 arch 块为空")
    else:
        bad = [a for a in arch if a not in ARCH_PLATFORMS]
        if bad:
            fails.append(f"[FAIL] C7 arch 含非法平台：{', '.join(sorted(bad))}")

    # C8 options/schema 一致性 + schema 类型合法性
    opt_keys = _block_top_keys(text, "options")
    sch_keys = _block_top_keys(text, "schema")
    if bool(opt_keys) != bool(sch_keys):
        side = "options" if opt_keys else "schema"
        fails.append(f"[FAIL] C8 有 options 就必须有 schema（或两者皆无）：仅检测到 {side}")
    elif opt_keys:
        only_opt = sorted(set(opt_keys) - set(sch_keys))
        only_sch = sorted(set(sch_keys) - set(opt_keys))
        if only_opt or only_sch:
            msg = "[FAIL] C8 options/schema 键不一致"
            if only_opt:
                msg += f"；仅 options 有：{', '.join(only_opt)}"
            if only_sch:
                msg += f"；仅 schema 有：{', '.join(only_sch)}"
            fails.append(msg)
        schema_vals = _block_top_values(text, "schema")
        for key in sorted(sch_keys):
            val = schema_vals.get(key, "")
            if not _valid_schema_type(val):
                fails.append(f"[FAIL] C8 schema 类型非法：{key} = {val[:50]}")

    # C9 image 字段：默认禁止；预构建模式（上游资料卡 # prebuilt: true）例外
    has_image = re.search(r"^image:", text, re.MULTILINE) is not None
    prebuilt = re.search(r"^#\s*prebuilt\s*:\s*true\b", text, re.MULTILINE) is not None
    if has_image and not prebuilt:
        fails.append("[FAIL] C9 本地 add-on 禁止 image: 字段（预构建模式需在上游资料卡加 `# prebuilt: true` 注释）")
    elif prebuilt and not has_image:
        warns.append("[WARN] W3 声明了 # prebuilt: true 但缺少 image: 字段")

    # C10 build.json 存在、合法 JSON、build_from 覆盖全部 arch
    build_path = addon_dir / "build.json"
    if not build_path.is_file():
        fails.append("[FAIL] C10 缺少 build.json")
    else:
        try:
            bd = json.loads(build_path.read_text(encoding="utf-8"))
        except Exception as exc:
            fails.append(f"[FAIL] C10 build.json 无法解析：{exc}")
            bd = None
        if bd is not None:
            bf = bd.get("build_from") if isinstance(bd, dict) else None
            if not isinstance(bf, dict) or not bf:
                fails.append("[FAIL] C10 build.json 缺少 build_from 对象")
            elif arch:
                not_covered = [a for a in arch if a not in bf]
                if not_covered:
                    fails.append(f"[FAIL] C10 build_from 未覆盖 arch：{', '.join(sorted(not_covered))}")

    # W1 url 含 example（占位）
    m = re.search(r"^url:\s*(.*)$", text, re.MULTILINE)
    if m and "example" in m.group(1).lower():
        warns.append("[WARN] W1 url 含 example（疑似占位 URL）")

    # W2 上游资料卡仍含 < > 未填占位
    card = _info_card_lines(text)
    if card and any("<" in ln or ">" in ln for ln in card):
        warns.append("[WARN] W2 上游资料卡仍含 <...> 未填占位")

    return fails, warns


# --------------------------------------------------------------------------- #
# manifest
# --------------------------------------------------------------------------- #
def load_manifest() -> dict:
    if not MANIFEST.is_file():
        return {}
    return json.loads(MANIFEST.read_text(encoding="utf-8"))


# --------------------------------------------------------------------------- #
# 运行与输出
# --------------------------------------------------------------------------- #
def print_report(slug: str, fails: list[str], warns: list[str]) -> None:
    print(f"== {slug} ==")
    for line in fails + warns:
        print(f"  {line}")
    print(f"[{'PASS' if not fails else 'FAIL'}] {slug}")


def run_one(addon_dir: Path, slug_label: str, as_json: bool, is_fixture: bool, source: str | None) -> int:
    fails, warns = check_addon(addon_dir, is_fixture, source)
    if as_json:
        print(json.dumps({"slug": slug_label, "fail": fails, "warn": warns,
                          "passed": not fails}, ensure_ascii=False, indent=2))
    else:
        print_report(slug_label, fails, warns)
    return 0 if not fails else 1


def run_all(slugs: list[str], as_json: bool, manifest: dict) -> int:
    addons = manifest.get("addons", {})
    results = []
    for slug in slugs:
        source = addons.get(slug, {}).get("source")
        addon_dir = ROOT / slug
        fails, warns = check_addon(addon_dir, False, source)
        results.append((slug, fails, warns))
        if not as_json:
            print_report(slug, fails, warns)
    if as_json:
        print(json.dumps([{"slug": s, "fail": f, "warn": w, "passed": not f}
                          for s, f, w in results], ensure_ascii=False, indent=2))
    else:
        passed = [s for s, f, _ in results if not f]
        failed = [s for s, f, _ in results if f]
        print("=== 自有 add-on 门禁批次结果 ===")
        print(f"通过 ({len(passed)}): {', '.join(passed) if passed else '无'}")
        if failed:
            print(f"失败 ({len(failed)}): {', '.join(failed)}")
    return 0 if all(not f for _, f, _ in results) else 1


# --------------------------------------------------------------------------- #
# CLI
# --------------------------------------------------------------------------- #
def main() -> int:
    parser = argparse.ArgumentParser(description="自有 add-on 编写门禁")
    parser.add_argument("slug", nargs="?", help="单 add-on slug（仓库根目录下）")
    parser.add_argument("--all", action="store_true", help="检查 manifest 中所有 source=local 的 add-on")
    parser.add_argument("--fixture", metavar="DIR", help="检查任意目录（测试用，无需 manifest）")
    parser.add_argument("--json", action="store_true", help="机器可读 JSON 输出（按 slug 一个对象；--all 为对象数组）")
    args = parser.parse_args()

    if args.fixture:
        target = Path(args.fixture)
        if not target.is_dir():
            print(f"错误：目录不存在 {target}")
            return 2
        return run_one(target, slug_label=target.name, as_json=args.json, is_fixture=True, source=None)

    try:
        manifest = load_manifest()
    except json.JSONDecodeError as exc:
        print(f"错误：addons-manifest.json 无法解析：{exc}")
        return 2
    if not manifest:
        print("错误：找不到 addons-manifest.json")
        return 2
    addons = manifest.get("addons")
    if not isinstance(addons, dict):
        print("错误：addons-manifest.json 的 addons 字段不是对象")
        return 2

    if args.all:
        slugs = sorted(s for s, e in addons.items() if isinstance(e, dict) and e.get("source") == "local")
        if not slugs:
            print("无 source=local 的自有 add-on")
            return 0
        return run_all(slugs, as_json=args.json, manifest=manifest)

    if args.slug:
        entry = addons.get(args.slug)
        source = entry.get("source") if isinstance(entry, dict) else None
        return run_one(ROOT / args.slug, slug_label=args.slug, as_json=args.json, is_fixture=False, source=source)

    parser.print_help()
    return 2


if __name__ == "__main__":
    sys.exit(main())
