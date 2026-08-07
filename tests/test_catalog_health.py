from __future__ import annotations

import importlib.util
import json
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / ".claude" / "scripts"


def load_catalog_health():
    path = SCRIPTS / "catalog_health.py"
    if not path.is_file():
        return None
    if str(SCRIPTS) not in sys.path:
        sys.path.insert(0, str(SCRIPTS))
    spec = importlib.util.spec_from_file_location("catalog_health", path)
    if spec is None or spec.loader is None:
        raise RuntimeError("could not load catalog_health")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


class CatalogHealthTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp_dir = tempfile.TemporaryDirectory()
        self.root = Path(self.temp_dir.name)

    def tearDown(self) -> None:
        self.temp_dir.cleanup()

    def make_repo(self, active: dict[str, bool], archived: set[str]) -> None:
        addons = {}
        for slug, guide in active.items():
            addon_dir = self.root / slug
            addon_dir.mkdir(parents=True)
            (addon_dir / "config.yaml").write_text("name: test\n", encoding="utf-8")
            marker = "<!-- zh-guide -->\n" if guide else ""
            (addon_dir / "README.md").write_text(marker + "# Test\n", encoding="utf-8")
            addons[slug] = {"source": "official", "zh_guide": guide}

        for slug in archived:
            archive_dir = self.root / "archive" / "addons" / slug
            archive_dir.mkdir(parents=True)
            (archive_dir / "config.yaml").write_text("name: archived\n", encoding="utf-8")

        (self.root / "catalog-policy.json").write_text(
            json.dumps({"archived_addons": sorted(archived)}), encoding="utf-8"
        )
        (self.root / "addons-manifest.json").write_text(
            json.dumps({"addons": addons}), encoding="utf-8"
        )
        active_count = len(active)
        guide_count = sum(active.values())
        stats = (
            f"- 📦 **{active_count} 个 add-on**：来自 official（{active_count}）。\n"
            f"- 📖 **中文指南**：{guide_count}/{active_count} 个 add-on。\n"
        )
        (self.root / "README.md").write_text(
            "before\n<!-- catalog-stats:start -->\n"
            + stats
            + "<!-- catalog-stats:end -->\nafter\n",
            encoding="utf-8",
        )

    def require_health(self):
        module = load_catalog_health()
        self.assertIsNotNone(module, "catalog_health module is missing")
        return module

    def test_collect_health_accepts_matching_active_catalog(self) -> None:
        self.make_repo(active={"alpha": True}, archived={"old"})

        facts, errors = self.require_health().collect_health(self.root)

        self.assertEqual(errors, [])
        self.assertEqual(facts.active_count, 1)
        self.assertEqual(facts.guide_count, 1)
        self.assertEqual(facts.source_counts, (("official", 1),))

    def test_collect_health_rejects_manifest_only_slug(self) -> None:
        self.make_repo(active={"alpha": False}, archived=set())
        manifest_path = self.root / "addons-manifest.json"
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        manifest["addons"]["missing"] = {"source": "official", "zh_guide": False}
        manifest_path.write_text(json.dumps(manifest), encoding="utf-8")

        _, errors = self.require_health().collect_health(self.root)

        self.assertIn("manifest-only addon: missing", errors)

    def test_collect_health_rejects_archived_slug_in_manifest_and_root(self) -> None:
        self.make_repo(active={"alpha": False, "old": False}, archived={"old"})

        _, errors = self.require_health().collect_health(self.root)

        self.assertIn("archived slug old is still in addons-manifest.json", errors)
        self.assertIn("archived slug old is still published at the repository root", errors)

    def test_collect_health_rejects_missing_archive_payload(self) -> None:
        self.make_repo(active={"alpha": False}, archived={"old"})
        (self.root / "archive" / "addons" / "old" / "config.yaml").unlink()

        _, errors = self.require_health().collect_health(self.root)

        self.assertIn("archived slug old is missing archive/addons/old/config.yaml", errors)

    def test_collect_health_rejects_guide_marker_drift(self) -> None:
        self.make_repo(active={"alpha": True}, archived=set())
        manifest_path = self.root / "addons-manifest.json"
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        manifest["addons"]["alpha"]["zh_guide"] = False
        manifest_path.write_text(json.dumps(manifest), encoding="utf-8")

        _, errors = self.require_health().collect_health(self.root)

        self.assertIn("zh_guide mismatch for alpha", errors)

    def test_replace_catalog_stats_changes_only_marker_block(self) -> None:
        readme = "before\n<!-- catalog-stats:start -->\nstale\n<!-- catalog-stats:end -->\nafter\n"

        actual = self.require_health().replace_catalog_stats(readme, "fresh")

        self.assertEqual(
            actual,
            "before\n<!-- catalog-stats:start -->\nfresh\n<!-- catalog-stats:end -->\nafter\n",
        )

    def test_replace_catalog_stats_rejects_missing_or_duplicate_markers(self) -> None:
        health = self.require_health()

        with self.assertRaisesRegex(ValueError, "exactly one"):
            health.replace_catalog_stats("no markers", "fresh")
        with self.assertRaisesRegex(ValueError, "exactly one"):
            health.replace_catalog_stats(
                "<!-- catalog-stats:start -->\n<!-- catalog-stats:end -->\n"
                "<!-- catalog-stats:start -->\n<!-- catalog-stats:end -->\n",
                "fresh",
            )


if __name__ == "__main__":
    unittest.main()
