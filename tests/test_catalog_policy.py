from __future__ import annotations

import importlib.util
import json
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / ".claude" / "scripts"


def load_catalog_policy():
    path = SCRIPTS / "catalog_policy.py"
    if not path.is_file():
        return None
    spec = importlib.util.spec_from_file_location("catalog_policy", path)
    if spec is None or spec.loader is None:
        raise RuntimeError("could not load catalog_policy")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


class CatalogPolicyTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp_dir = tempfile.TemporaryDirectory()
        self.root = Path(self.temp_dir.name)

    def tearDown(self) -> None:
        self.temp_dir.cleanup()

    def write_policy(self, archived_addons: object) -> None:
        (self.root / "catalog-policy.json").write_text(
            json.dumps({"archived_addons": archived_addons}), encoding="utf-8"
        )

    def require_policy(self):
        module = load_catalog_policy()
        self.assertIsNotNone(module, "catalog_policy module is missing")
        return module

    def test_load_archived_slugs_returns_unique_slug_set(self) -> None:
        self.write_policy(["old-one", "old-two"])

        actual = self.require_policy().load_archived_slugs(self.root)

        self.assertEqual(actual, {"old-one", "old-two"})

    def test_load_archived_slugs_rejects_duplicate_entries(self) -> None:
        self.write_policy(["old-one", "old-one"])

        with self.assertRaisesRegex(ValueError, "contains duplicates"):
            self.require_policy().load_archived_slugs(self.root)

    def test_load_archived_slugs_rejects_non_string_entries(self) -> None:
        self.write_policy(["old-one", 42])

        with self.assertRaisesRegex(ValueError, "must be a string list"):
            self.require_policy().load_archived_slugs(self.root)


if __name__ == "__main__":
    unittest.main()
