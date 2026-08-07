from __future__ import annotations

import importlib.util
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / ".claude" / "scripts"


def load_sync_addons():
    if str(SCRIPTS) not in sys.path:
        sys.path.insert(0, str(SCRIPTS))
    path = SCRIPTS / "sync-addons.py"
    spec = importlib.util.spec_from_file_location("sync_addons", path)
    if spec is None or spec.loader is None:
        raise RuntimeError("could not load sync-addons")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


class SyncAddonsPolicyTests(unittest.TestCase):
    def test_exclude_archived_owners_keeps_only_publishable_slugs(self) -> None:
        sync_addons = load_sync_addons()
        owners = {
            "active": ("official", Path("/tmp/active"), "1.0.0"),
            "obsolete": ("frenck", Path("/tmp/obsolete"), "1.0.0"),
        }

        self.assertTrue(
            hasattr(sync_addons, "exclude_archived_owners"),
            "sync-addons must expose exclude_archived_owners",
        )
        actual = sync_addons.exclude_archived_owners(owners, {"obsolete"})

        self.assertEqual(set(actual), {"active"})


if __name__ == "__main__":
    unittest.main()
