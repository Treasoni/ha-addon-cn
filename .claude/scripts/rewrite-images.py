#!/usr/bin/env python3
"""
批量改写本商店 add-on 的 config.yaml `image:` 到国内镜像源（镜像地址重写）。

用法：
  python .claude/scripts/rewrite-images.py [--dry-run] [--mirror HOST]

默认行为：探测候选镜像源（或 --mirror 指定），把商店根目录下所有非 source:local、
镜像主机是 ghcr.io 或已知镜像源的 config.yaml 改写为所选镜像源前缀。
幂等：已是目标镜像源则不变；已改写过的（如换源场景）会被正确迁移。

规则见 .claude/rules/common/mirror-sources.md。
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

import registry_mirror as rm

ROOT = Path(__file__).resolve().parent.parent.parent
MANIFEST = ROOT / "addons-manifest.json"


def load_manifest() -> dict:
    if MANIFEST.exists():
        try:
            return json.loads(MANIFEST.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            return {}
    return {}


def local_slugs() -> set[str]:
    m = load_manifest()
    return {s for s, e in m.get("addons", {}).items() if e.get("source") == "local"}


def _collect_probes() -> list[tuple[str, str]]:
    """从商店里挑至多 3 个不同来源的 ghcr 镜像作为探测样本 (repo, version)。"""
    m = load_manifest()
    by_source: dict[str, list[tuple[str, str]]] = {}
    for cfg in sorted(ROOT.glob("*/config.yaml")):
        slug = cfg.parent.name
        src = m.get("addons", {}).get(slug, {}).get("source", "?")
        img, ver = rm.image_fields(cfg)
        if img and rm.classify(img) == "ghcr" and ver:
            by_source.setdefault(src, []).append((img, ver))
    probes: list[tuple[str, str]] = []
    for _, items in by_source.items():
        if len(probes) >= 3:
            break
        if items:
            img, ver = items[0]
            probes.append((rm.image_repo(img), ver))
    return probes


def main() -> int:
    ap = argparse.ArgumentParser(description="把 add-on config.yaml 的 image 改写为国内镜像源")
    ap.add_argument("--dry-run", action="store_true", help="只报告，不写文件")
    ap.add_argument("--mirror", help="指定镜像源主机，跳过自动探测")
    args = ap.parse_args()

    mirror = args.mirror
    if not mirror:
        probes = _collect_probes()
        if not probes:
            print("找不到可探测的 ghcr 镜像，请用 --mirror 显式指定镜像源。")
            return 2
        mirror = rm.pick_mirror(probes)
        if not mirror:
            print("所有候选镜像源探测失败，中止（可 --mirror 强制指定）。")
            return 1

    local = local_slugs()
    changed: list[str] = []
    for cfg in sorted(ROOT.glob("*/config.yaml")):
        slug = cfg.parent.name
        if slug in local:
            continue  # source: local 永不触碰
        text = cfg.read_text(encoding="utf-8", errors="replace")
        new = rm.transform_yaml(text, mirror)
        if new == text:
            continue
        if not args.dry_run:
            cfg.write_text(new, encoding="utf-8")
        changed.append(slug)

    print(
        f"\n改写 {len(changed)} 个 config.yaml -> {mirror}"
        + ("（dry-run，未写盘）" if args.dry_run else "")
    )
    for s in changed:
        print("  ", s)
    return 0


if __name__ == "__main__":
    sys.exit(main())
