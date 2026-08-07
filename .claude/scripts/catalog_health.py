#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import sys
from dataclasses import dataclass
from pathlib import Path

import catalog_policy


ROOT = Path(__file__).resolve().parent.parent.parent
MANIFEST_FILE = "addons-manifest.json"
README_FILE = "README.md"
GUIDE_MARKER = "<!-- zh-guide -->"
STATS_START = "<!-- catalog-stats:start -->"
STATS_END = "<!-- catalog-stats:end -->"
NON_ADDON_DIRECTORIES = {"archive", "docs", "workspace"}


if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass


@dataclass(frozen=True)
class CatalogFacts:
    active_count: int
    guide_count: int
    source_counts: tuple[tuple[str, int], ...]


def discover_active_addons(root: Path) -> set[str]:
    return {
        child.name
        for child in root.iterdir()
        if child.is_dir()
        and not child.name.startswith(".")
        and child.name not in NON_ADDON_DIRECTORIES
        and (child / "config.yaml").is_file()
    }


def has_zh_guide(addon_dir: Path) -> bool:
    readme = addon_dir / README_FILE
    return readme.is_file() and GUIDE_MARKER in readme.read_text(
        encoding="utf-8", errors="replace"
    )


def load_manifest(root: Path) -> dict:
    manifest_path = root / MANIFEST_FILE
    try:
        payload = json.loads(manifest_path.read_text(encoding="utf-8"))
    except FileNotFoundError as exc:
        raise ValueError(f"missing {MANIFEST_FILE}") from exc
    except json.JSONDecodeError as exc:
        raise ValueError(f"invalid {MANIFEST_FILE}: {exc.msg}") from exc
    if not isinstance(payload.get("addons"), dict):
        raise ValueError(f"{MANIFEST_FILE} addons must be an object")
    return payload


def build_facts(addons: dict[str, object]) -> CatalogFacts:
    source_counts: dict[str, int] = {}
    guide_count = 0
    for entry in addons.values():
        if not isinstance(entry, dict):
            continue
        source = entry.get("source")
        if isinstance(source, str):
            source_counts[source] = source_counts.get(source, 0) + 1
        guide_count += entry.get("zh_guide") is True
    return CatalogFacts(
        active_count=len(addons),
        guide_count=guide_count,
        source_counts=tuple(sorted(source_counts.items())),
    )


def render_catalog_stats(facts: CatalogFacts) -> str:
    sources = "、".join(f"{source}（{count}）" for source, count in facts.source_counts)
    return (
        f"- 📦 **{facts.active_count} 个 add-on**：来自 {sources}。\n"
        f"- 📖 **中文指南**：{facts.guide_count}/{facts.active_count} 个 add-on。"
    )


def replace_catalog_stats(readme: str, block: str) -> str:
    if readme.count(STATS_START) != 1 or readme.count(STATS_END) != 1:
        raise ValueError("README catalog stats markers must appear exactly one time each")
    start = readme.index(STATS_START)
    end = readme.index(STATS_END)
    if end < start:
        raise ValueError("README catalog stats markers are out of order")
    before = readme[:start]
    after = readme[end + len(STATS_END) :]
    return f"{before}{STATS_START}\n{block.rstrip()}\n{STATS_END}{after}"


def read_catalog_stats(readme: str) -> str:
    if readme.count(STATS_START) != 1 or readme.count(STATS_END) != 1:
        raise ValueError("README catalog stats markers must appear exactly one time each")
    start = readme.index(STATS_START) + len(STATS_START)
    end = readme.index(STATS_END)
    if end < start:
        raise ValueError("README catalog stats markers are out of order")
    return readme[start:end].strip()


def collect_health(root: Path) -> tuple[CatalogFacts, list[str]]:
    manifest = load_manifest(root)
    addons = manifest["addons"]
    archived = catalog_policy.load_archived_slugs(root)
    active_dirs = discover_active_addons(root)
    manifest_slugs = set(addons)
    errors: list[str] = []

    for slug in sorted(manifest_slugs - active_dirs):
        errors.append(f"manifest-only addon: {slug}")
    for slug in sorted(active_dirs - manifest_slugs):
        errors.append(f"root-only addon: {slug}")
    for slug in sorted(archived):
        if slug in manifest_slugs:
            errors.append(f"archived slug {slug} is still in addons-manifest.json")
        if slug in active_dirs:
            errors.append(f"archived slug {slug} is still published at the repository root")
        if not (root / "archive" / "addons" / slug / "config.yaml").is_file():
            errors.append(f"archived slug {slug} is missing archive/addons/{slug}/config.yaml")
    for slug in sorted(manifest_slugs & active_dirs):
        entry = addons[slug]
        marked = isinstance(entry, dict) and entry.get("zh_guide") is True
        if marked != has_zh_guide(root / slug):
            errors.append(f"zh_guide mismatch for {slug}")

    facts = build_facts(addons)
    readme_path = root / README_FILE
    try:
        current_stats = read_catalog_stats(readme_path.read_text(encoding="utf-8"))
    except (FileNotFoundError, ValueError) as exc:
        errors.append(str(exc))
    else:
        if current_stats != render_catalog_stats(facts):
            errors.append("README catalog stats block is out of date")
    return facts, errors


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate catalog publication invariants")
    parser.add_argument("--root", type=Path, default=ROOT, help="repository root")
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--check", action="store_true", help="validate the catalog")
    mode.add_argument("--write-readme", action="store_true", help="refresh generated README statistics")
    args = parser.parse_args()

    try:
        facts, errors = collect_health(args.root)
    except ValueError as exc:
        print(f"catalog-health: {exc}")
        return 1

    stats_error = "README catalog stats block is out of date"
    blocking_errors = [error for error in errors if error != stats_error]
    if args.write_readme and not blocking_errors:
        readme_path = args.root / README_FILE
        readme_path.write_text(
            replace_catalog_stats(
                readme_path.read_text(encoding="utf-8"), render_catalog_stats(facts)
            ),
            encoding="utf-8",
        )
        return 0

    if errors:
        for error in errors:
            print(f"catalog-health: {error}")
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
