from __future__ import annotations

import json
from pathlib import Path


POLICY_FILE = "catalog-policy.json"


def load_archived_slugs(root: Path) -> set[str]:
    """Load the unique set of add-on slugs excluded from publication."""
    policy_path = root / POLICY_FILE
    try:
        payload = json.loads(policy_path.read_text(encoding="utf-8"))
    except FileNotFoundError as exc:
        raise ValueError(f"missing {POLICY_FILE}") from exc
    except json.JSONDecodeError as exc:
        raise ValueError(f"invalid {POLICY_FILE}: {exc.msg}") from exc

    slugs = payload.get("archived_addons")
    if not isinstance(slugs, list) or any(not isinstance(slug, str) for slug in slugs):
        raise ValueError(f"{POLICY_FILE} archived_addons must be a string list")
    if len(slugs) != len(set(slugs)):
        raise ValueError(f"{POLICY_FILE} archived_addons contains duplicates")
    return set(slugs)
