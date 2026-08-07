#!/usr/bin/env python3
"""
Home Assistant Add-on 商店同步脚本。

把上游 Home Assistant add-on 仓库中的 add-on 全量镜像进本仓库（商店根目录），
维护 addons-manifest.json 作为同步基线。同时支持：
  - 从模板脚手架新建自有 add-on（--new-addon），标记 source=local，永不被同步触碰；
  - 输出中文指南状态（--zh-status）；
  - 生成 README 用的 add-on 列表（--readme-list）。

规则要点：
  - README.md 是"本地维护文件"：vendored add-on 已有本地 README.md 时永不被上游覆盖；
  - 只复制上游 add-on 文件夹，不复制上游根级工具文件；
  - 有未提交本地修改（git diff 相对 HEAD）的 add-on 会跳过并警告；
  - source=local 的 add-on 永不处理、永不删除；
  - 镜像地址重写（post-sync transform）：同步后把 config.yaml 的 image 主机改写为
    国内镜像源（registry_mirror.py），改写后再对比避免误报 updated，天然幂等。

无第三方依赖（不依赖 PyYAML）。
"""

from __future__ import annotations

import argparse
import datetime
import filecmp
import json
import re
import shutil
import subprocess
import sys
from pathlib import Path

import registry_mirror as rm  # 镜像地址重写共享模块（同目录）

ROOT = Path(__file__).resolve().parent.parent.parent
MANIFEST = ROOT / "addons-manifest.json"
REPOSITORY = ROOT / "repository.json"
CACHE = ROOT / ".cache" / "upstream"
SKILL_DIR = ROOT / ".claude" / "skills" / "hassio-addon-sync"
TEMPLATE_DIR = SKILL_DIR / "templates" / "new-addon"

ZH_MARKER = "<!-- zh-guide -->"

DEFAULT_SOURCES = [
    {"id": "alexbelgium", "repo": "alexbelgium/hassio-addons", "branch": "master", "priority": 1, "license": "MIT"},
    {"id": "official", "repo": "home-assistant/addons", "branch": "master", "priority": 2, "license": "Apache-2.0"},
    {"id": "frenck", "repo": "hassio-addons/repository", "branch": "master", "priority": 3, "license": "MIT"},
]

def log(msg: str) -> None:
    print(msg)


def run_git(args: list[str], cwd: Path) -> subprocess.CompletedProcess:
    return subprocess.run(
        ["git", "-C", str(cwd)] + args,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
    )


# --------------------------------------------------------------------------- #
# Manifest helpers
# --------------------------------------------------------------------------- #
def load_manifest() -> dict:
    if MANIFEST.exists():
        return json.loads(MANIFEST.read_text(encoding="utf-8"))
    store = {}
    if REPOSITORY.exists():
        try:
            store = json.loads(REPOSITORY.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            store = {}
    return {
        "schema_version": 1,
        "store": store,
        "sources": DEFAULT_SOURCES,
        "synced_at": None,
        "addons": {},
        "conflicts": [],
    }


def save_manifest(m: dict) -> None:
    MANIFEST.write_text(
        json.dumps(m, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )


def source_map(m: dict) -> dict:
    return {s["id"]: s for s in m.get("sources", DEFAULT_SOURCES)}


# --------------------------------------------------------------------------- #
# Upstream fetch (shallow clone)
# --------------------------------------------------------------------------- #
def ensure_upstream(src: dict) -> Path:
    repo = src["repo"]
    branch = src["branch"]
    target = CACHE / src["id"]
    url = f"https://github.com/{repo}.git"
    if not (target / ".git").exists():
        log(f"[fetch] 浅克隆 {repo} ({branch}) -> {target}")
        proc = run_git(
            ["clone", "--depth", "1", "--single-branch", "--branch", branch, url, str(target)],
            cwd=ROOT,
        )
        if proc.returncode != 0:
            raise RuntimeError(f"克隆失败 {repo}: {proc.stderr.strip() or proc.stdout.strip()}")
    else:
        log(f"[fetch] 更新缓存 {repo} ({branch})")
        for cmd in (
            ["fetch", "--depth", "1", "origin", branch],
            ["reset", "--hard", f"origin/{branch}"],
        ):
            proc = run_git(cmd, cwd=target)
            if proc.returncode != 0:
                raise RuntimeError(f"更新失败 {repo}: {proc.stderr.strip()}")
    return target


def upstream_last_commit(target: Path) -> str:
    proc = run_git(["rev-parse", "HEAD"], cwd=target)
    return proc.stdout.strip() if proc.returncode == 0 else ""


# --------------------------------------------------------------------------- #
# Add-on discovery / YAML field
# --------------------------------------------------------------------------- #
def find_addons(upstream_root: Path) -> dict[str, Path]:
    """返回 {slug: 目录路径}，只认直接子目录中含 config.yaml 的文件夹。"""
    out = {}
    if not upstream_root.is_dir():
        return out
    for child in upstream_root.iterdir():
        if child.is_dir() and (child / "config.yaml").is_file():
            out[child.name] = child
    return out


def yaml_field(config_path: Path, field: str) -> str | None:
    text = config_path.read_text(encoding="utf-8", errors="replace")
    m = re.search(rf"^{field}:\s*[\"']?([^\"'\s#]+)", text, re.MULTILINE)
    return m.group(1) if m else None


# --------------------------------------------------------------------------- #
# Git dirty check (tracked modifications vs HEAD)
# --------------------------------------------------------------------------- #
def is_dirty(local_dir: Path) -> bool:
    rel = local_dir.relative_to(ROOT).as_posix()
    proc = run_git(["diff", "--quiet", "HEAD", "--", rel], cwd=ROOT)
    # returncode 0 = 无差异(干净)；1 = 有差异(dirty)
    return proc.returncode != 0


# --------------------------------------------------------------------------- #
# Copy semantics
# --------------------------------------------------------------------------- #
def files_equal(a: Path, b: Path) -> bool:
    try:
        return filecmp.cmp(a, b, shallow=False)
    except OSError:
        return False


def copy_addon_dir(upstream_dir: Path, local_dir: Path, summary: dict, mirror: str | None = None) -> str:
    """复制一个新 add-on 目录（本地不存在）。返回 'added'。"""
    shutil.copytree(upstream_dir, local_dir, dirs_exist_ok=False)
    if mirror:
        _rewrite_config(local_dir / "config.yaml", mirror)
    summary["added"].append(local_dir.name)
    return "added"


def _rewrite_config(cfg_path: Path, mirror: str) -> None:
    """对 config.yaml 应用镜像地址重写（幂等，改写后不变则不动）。"""
    try:
        text = cfg_path.read_text(encoding="utf-8", errors="replace")
    except OSError:
        return
    new = rm.transform_yaml(text, mirror)
    if new != text:
        cfg_path.write_text(new, encoding="utf-8")


def sync_existing_dir(upstream_dir: Path, local_dir: Path, summary: dict, dry_run: bool = False, mirror: str | None = None) -> str:
    """
    同步已有 add-on：只 add/overwrite 上游变更文件，绝不删除本地文件，
    README.md 若本地已有则永不覆盖（本地维护）。返回 'updated'/'unchanged'。

    config.yaml 先过镜像地址重写（transform）再与本地对比/写入：本地是改写版、
    上游是原版，只有真实上游变更才算 updated（幂等，不误报）。
    """
    changed = 0
    for up_file in upstream_dir.rglob("*"):
        if not up_file.is_file():
            continue
        rel = up_file.relative_to(upstream_dir).as_posix()
        dst = local_dir / rel
        if rel == "README.md" and dst.exists():
            continue  # 本地维护 README，永不覆盖
        if rel == "config.yaml" and mirror:
            up_text = up_file.read_text(encoding="utf-8", errors="replace")
            up_norm = rm.transform_yaml(up_text, mirror)
            try:
                same = dst.exists() and dst.read_text(encoding="utf-8", errors="replace") == up_norm
            except OSError:
                same = False
        else:
            same = dst.exists() and files_equal(up_file, dst)
        if same:
            continue
        changed += 1
        if not dry_run:
            dst.parent.mkdir(parents=True, exist_ok=True)
            if rel == "config.yaml" and mirror:
                dst.write_text(up_norm, encoding="utf-8")
            else:
                shutil.copy2(up_file, dst)
    if changed:
        summary["updated"].append(local_dir.name)
        return "updated"
    summary["unchanged"].append(local_dir.name)
    return "unchanged"


def pick_sync_mirror(srcs: list[dict], owners: dict) -> str | None:
    """按源优先级挑至多 3 个 ghcr 镜像作探测样本，选一个可用国内镜像源。

    每次同步复验一次镜像源（每 registry 打一次 manifest，很便宜）。
    无 ghcr 镜像或全失败时返回 None，调用方回退默认镜像源。
    """
    probes: list[tuple[str, str]] = []
    for src in sorted(srcs, key=lambda s: s.get("priority", 99)):
        sid = src["id"]
        if len(probes) >= 3:
            break
        for slug, (osid, up_dir, up_ver) in sorted(owners.items()):
            if osid != sid:
                continue
            img = yaml_field(up_dir / "config.yaml", "image")
            if img and rm.classify(img) == "ghcr" and up_ver:
                probes.append((rm.image_repo(img), up_ver))
                break
    if not probes:
        return None
    return rm.pick_mirror(probes, timeout=15.0)


def has_zh_guide(local_dir: Path) -> bool:
    readme = local_dir / "README.md"
    if not readme.is_file():
        return False
    try:
        return ZH_MARKER in readme.read_text(encoding="utf-8", errors="replace")
    except OSError:
        return False


# --------------------------------------------------------------------------- #
# Main sync
# --------------------------------------------------------------------------- #
def cmd_sync(dry_run: bool = False) -> int:
    manifest = load_manifest()
    srcs = manifest.get("sources", DEFAULT_SOURCES)
    addons = manifest.setdefault("addons", {})
    conflicts = manifest.setdefault("conflicts", [])

    summary = {
        "added": [],
        "updated": [],
        "unchanged": [],
        "skipped": [],
        "deleted": [],
        "conflicts": [],
    }

    # 1) 拉取全部上游并建立 slug -> (source, upstream_dir) 归属表（按优先级）
    owners: dict[str, tuple[str, Path, str]] = {}  # slug -> (source_id, upstream_addon_dir, upstream_version)
    upstream_roots = {}
    for src in sorted(srcs, key=lambda s: s.get("priority", 99)):
        sid = src["id"]
        target = ensure_upstream(src)
        upstream_roots[sid] = (target, upstream_last_commit(target))
        for slug, addon_dir in find_addons(target).items():
            ver = yaml_field(addon_dir / "config.yaml", "version") or ""
            if slug in owners:
                conflict = next((c for c in conflicts if c.get("slug") == slug), None)
                if conflict is None:
                    conflict = {"slug": slug, "won": owners[slug][0], "skipped": [sid]}
                    conflicts.append(conflict)
                else:
                    conflict.setdefault("skipped", [])
                    if sid not in conflict["skipped"]:
                        conflict["skipped"].append(sid)
                summary["conflicts"].append(slug)
                continue
            owners[slug] = (sid, addon_dir, ver)

    # 1.5) 选定国内镜像源（每次同步复验一次；挂则回退默认并告警）
    mirror = pick_sync_mirror(srcs, owners)
    if mirror:
        log(f"[mirror] 本次同步使用镜像源: {mirror}")
    else:
        mirror = rm.KNOWN_MIRRORS[0]
        log(f"[mirror] 警告：无法验证镜像源，回退默认 {mirror}（可用 check-images.py 复核）")

    # 2) 同步每个归属 add-on
    seen_slugs = set()
    for slug, (sid, up_dir, up_ver) in sorted(owners.items()):
        seen_slugs.add(slug)
        local_dir = ROOT / slug
        entry = addons.get(slug)
        if not local_dir.exists():
            if dry_run:
                log(f"  [dry] 新增 {slug} (来自 {sid})")
                summary["added"].append(slug)
                continue
            copy_addon_dir(up_dir, local_dir, summary, mirror)
            addons[slug] = {
                "source": sid,
                "upstream_version": up_ver,
                "local_version": up_ver,
                "synced_at": now_iso(),
                "zh_guide": False,
            }
        else:
            if is_dirty(local_dir):
                summary["skipped"].append(slug)
                log(f"  [skip] {slug}：目录有未提交本地修改，跳过（不覆盖）")
                continue
            status = sync_existing_dir(up_dir, local_dir, summary, dry_run=dry_run, mirror=mirror)
            if not dry_run and status == "updated":
                addons[slug] = {
                    "source": sid,
                    "upstream_version": up_ver,
                    "local_version": up_ver,
                    "synced_at": now_iso(),
                    "zh_guide": has_zh_guide(local_dir),
                }

    # 3) 删除策略：上游已删除、本地干净且非 source=local 的 add-on
    for slug in list(addons.keys()):
        entry = addons[slug]
        if entry.get("source") == "local":
            continue  # 自有 add-on，永不处理
        if slug in seen_slugs:
            continue
        local_dir = ROOT / slug
        if not local_dir.exists():
            addons.pop(slug)
            continue
        if is_dirty(local_dir):
            log(f"  [keep] {slug}：上游已删除，但本地有修改/中文指南，保留")
            summary["skipped"].append(slug)
            continue
        if dry_run:
            log(f"  [dry] 删除 {slug}（上游已移除）")
            summary["deleted"].append(slug)
            continue
        shutil.rmtree(local_dir)
        addons.pop(slug)
        summary["deleted"].append(slug)

    # 4) 刷新 zh_guide 标记（与磁盘实际保持一致）并更新 manifest 元信息
    if not dry_run:
        for slug, entry in addons.items():
            if entry.get("source") == "local":
                continue
            entry["zh_guide"] = has_zh_guide(ROOT / slug)
        per_source = {}
        for sid, (target, commit) in upstream_roots.items():
            per_source[sid] = {"last_commit": commit}
        manifest["upstream"] = per_source
        manifest["synced_at"] = now_iso()
        manifest["image_mirror"] = mirror
        manifest["addons"] = addons
        manifest["conflicts"] = conflicts
        save_manifest(manifest)

    print_summary(summary, dry_run=dry_run)
    return 0


def print_summary(summary: dict, dry_run: bool = False) -> None:
    prefix = "[dry] " if dry_run else ""
    print(f"\n=== 同步摘要 {prefix}===")
    for key, label in (
        ("added", "新增"),
        ("updated", "更新"),
        ("unchanged", "未变化"),
        ("skipped", "跳过(本地已修改)"),
        ("deleted", "删除"),
        ("conflicts", "同名冲突"),
    ):
        items = summary[key]
        shown = ", ".join(sorted(set(items))[:40])
        more = f" …共 {len(set(items))} 个" if len(set(items)) > 40 else ""
        print(f"{label} ({len(set(items))}): {shown}{more}")


def cmd_zh_status() -> int:
    manifest = load_manifest()
    have, missing = [], []
    for slug, entry in sorted(manifest.get("addons", {}).items()):
        if entry.get("source") == "local":
            continue
        local_dir = ROOT / slug
        (have if has_zh_guide(local_dir) else missing).append(slug)
    print(f"=== 中文指南状态 ===\n已有 ({len(have)}): {', '.join(have)}")
    print(f"\n缺失 ({len(missing)}): {', '.join(missing)}")
    return 0


def cmd_readme_list() -> int:
    manifest = load_manifest()
    by_source: dict[str, list[str]] = {}
    for slug, entry in sorted(manifest.get("addons", {}).items()):
        src = entry.get("source", "?")
        by_source.setdefault(src, []).append(slug)
    print("### Add-on 列表（按源分组）\n")
    for src in sorted(by_source, key=lambda s: source_map(manifest).get(s, {}).get("priority", 99)):
        slugs = by_source[src]
        meta = source_map(manifest).get(src, {})
        print(f"#### {src}（{meta.get('repo', '?')}）— {len(slugs)} 个")
        print(", ".join(slugs))
        print()
    return 0


# --------------------------------------------------------------------------- #
# New add-on scaffold
# --------------------------------------------------------------------------- #
def cmd_new_addon(slug: str, name: str | None, version: str) -> int:
    if not re.fullmatch(r"[a-z0-9][a-z0-9_-]*", slug):
        log(f"错误：slug 只能包含小写字母、数字、连字符、下划线，且以字母/数字开头：{slug}")
        return 1
    local_dir = ROOT / slug
    if local_dir.exists():
        log(f"错误：目录已存在：{slug}")
        return 1
    if not TEMPLATE_DIR.is_dir():
        log(f"错误：找不到模板目录 {TEMPLATE_DIR}")
        return 1

    display_name = name or slug.replace("-", " ").replace("_", " ").title()
    shutil.copytree(TEMPLATE_DIR, local_dir)
    for f in local_dir.rglob("*"):
        if f.is_file():
            text = f.read_text(encoding="utf-8", errors="replace")
            text = (
                text.replace("__SLUG__", slug)
                .replace("__NAME__", display_name)
                .replace("__VERSION__", version)
            )
            f.write_text(text, encoding="utf-8")

    manifest = load_manifest()
    manifest.setdefault("addons", {})[slug] = {
        "source": "local",
        "local_version": version,
        "synced_at": now_iso(),
        "zh_guide": False,
    }
    save_manifest(manifest)
    log(f"已创建自有 add-on：{slug}（source=local，同步脚本永不触碰）")
    log(f"下一步：编辑 {slug}/config.yaml 完善选项与 schema，补 icon.png/logo.png。")
    return 0


def now_iso() -> str:
    return datetime.datetime.now(datetime.timezone.utc).isoformat(timespec="seconds")


# --------------------------------------------------------------------------- #
def main() -> int:
    parser = argparse.ArgumentParser(description="HA Add-on 商店同步/脚手架")
    parser.add_argument("--dry-run", action="store_true", help="只报告变更，不写入")
    parser.add_argument("--new-addon", metavar="SLUG", help="从模板新建自有 add-on")
    parser.add_argument("--name", metavar="NAME", help="新 add-on 显示名（配合 --new-addon）")
    parser.add_argument("--version", default="0.1.0", help="新 add-on 版本（默认 0.1.0）")
    parser.add_argument("--zh-status", action="store_true", help="输出中文指南状态")
    parser.add_argument("--readme-list", action="store_true", help="输出 README 用 add-on 列表")
    args = parser.parse_args()

    if args.new_addon:
        return cmd_new_addon(args.new_addon, args.name, args.version)
    if args.zh_status:
        return cmd_zh_status()
    if args.readme_list:
        return cmd_readme_list()
    return cmd_sync(dry_run=args.dry_run)


if __name__ == "__main__":
    sys.exit(main())
