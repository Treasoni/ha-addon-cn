#!/usr/bin/env python3
"""
校验本商店所有 add-on 的镜像引用可拉取（镜像可达性门禁）。

- ghcr 类（ghcr.io 或已知镜像源前缀）：经当前镜像源以真实 version 探测，硬校验，
  失败退出码非 0，可作 CI / 发布门禁。
- Docker Hub 类（官方 24 个，homeassistant/{arch}-addon-x）：查 hub.docker.com tags
  存在性，仅提示，不阻断（可达性因 HA 主机而异）。
- 其他（quay.io / lscr.io 等）：跳过。

用法：
  python .codex/scripts/check-images.py [--mirror HOST] [--workers N] [--json]
镜像源解析顺序：--mirror > addons-manifest.json 的 image_mirror > KNOWN_MIRRORS[0]。
"""
from __future__ import annotations

import argparse
import json
import sys
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

import registry_mirror as rm

ROOT = Path(__file__).resolve().parent.parent.parent
MANIFEST = ROOT / "addons-manifest.json"


def resolve_mirror(override: str | None) -> str:
    if override:
        return override.rstrip("/")
    try:
        m = json.loads(MANIFEST.read_text(encoding="utf-8"))
        stored = m.get("image_mirror")
        if stored:
            return stored
    except (OSError, json.JSONDecodeError):
        pass
    return rm.KNOWN_MIRRORS[0]


def main() -> int:
    ap = argparse.ArgumentParser(description="校验商店镜像引用可达性")
    ap.add_argument("--mirror", help="指定镜像源主机（默认读 manifest.image_mirror）")
    ap.add_argument("--workers", type=int, default=8, help="并发探测数（默认 8）")
    ap.add_argument("--json", action="store_true", help="输出 JSON 摘要")
    args = ap.parse_args()

    mirror = resolve_mirror(args.mirror)
    try:
        m = json.loads(MANIFEST.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        m = {}
    local = {s for s, e in m.get("addons", {}).items() if e.get("source") == "local"}

    configs = sorted(ROOT.glob("*/config.yaml"))
    results: list[tuple[str, str, str, bool, str]] = []  # (slug, class, image, ok, detail)

    def _run(cfg: Path) -> tuple[str, str, str, bool, str]:
        slug = cfg.parent.name
        img, _ = rm.image_fields(cfg)
        cls = rm.classify(img or "")
        if slug in local:
            return slug, cls, img or "", True, "source:local，跳过"
        if cls == "ghcr":
            _, ok, detail = rm.check_ghcr(cfg, mirror)
            return slug, cls, img or "", ok, detail
        if cls == "dockerhub":
            _, ok, detail = rm.check_docker_hub(cfg)
            return slug, cls, img or "", ok, detail
        return slug, cls, img or "", True, "其他 registry，跳过"

    with ThreadPoolExecutor(max_workers=max(1, args.workers)) as pool:
        results = list(pool.map(_run, configs))

    fails = [r for r in results if not r[3]]
    warnings = [
        r for r in results if r[1] == "dockerhub" and not r[3]
    ]
    ghcr_ok = sum(1 for r in results if r[1] == "ghcr" and r[3])
    ghcr_fail = [r for r in results if r[1] == "ghcr" and not r[3]]
    hub_ok = sum(1 for r in results if r[1] == "dockerhub" and r[3])

    if args.json:
        print(json.dumps({
            "mirror": mirror,
            "total": len(results),
            "ghcr_ok": ghcr_ok,
            "ghcr_fail": [r[0] for r in ghcr_fail],
            "dockerhub_ok": hub_ok,
            "dockerhub_missing": [r[0] for r in warnings],
            "ok": len(ghcr_fail) == 0,
        }, ensure_ascii=False, indent=2))
        return 1 if ghcr_fail else 0

    print(f"\n=== 镜像可达性校验（镜像源: {mirror}）===")
    print(f"ghcr 类通过: {ghcr_ok}/{sum(1 for r in results if r[1]=='ghcr')}")
    print(f"Docker Hub 类存在: {hub_ok}/{sum(1 for r in results if r[1]=='dockerhub')}")
    if fails:
        print("\n[FAIL] ghcr 镜像经镜像源不可拉:")
        for slug, cls, img, ok, detail in fails:
            print(f"  {slug:24s} {img:52s} {detail}")
    if warnings:
        print("\n[WARN] Docker Hub 镜像未在 hub.docker.com 查到（可达性因主机而异，仅提示）:")
        for slug, cls, img, ok, detail in warnings:
            print(f"  {slug:24s} {img:52s} {detail}")
    print("\n" + ("全部 ghcr 镜像可达 ✅" if not ghcr_fail else "存在不可达镜像 ❌"))
    return 1 if ghcr_fail else 0


if __name__ == "__main__":
    sys.exit(main())
