# Catalog Governance Design

## Goal

Make the published Home Assistant add-on catalog self-consistent and prevent new container-supply-chain violations, without guessing replacement versions for existing vendored add-ons.

## Scope

This change will:

- remove nine explicitly archived add-ons from the published root catalog while retaining their files under `archive/addons/`;
- prevent `sync-addons.py` from reintroducing archived slugs on a later upstream sync;
- make catalog counts and Chinese-guide status in `README.md` generated from the manifest and checked in CI;
- add a versioned Docker policy baseline so existing vendored violations are visible but do not block the repository, while new violations do;
- flag shell-piped remote installers and remote Docker `ADD` instructions alongside the existing Docker checks;
- run the catalog and Docker checks in GitHub Actions.

This change will not pin the current upstream images, change the contents of vendored add-ons, or update images from the network. Those changes need per-add-on compatibility verification and are tracked as baseline debt.

## Catalog Policy Module

`catalog-policy.json` is the single source of truth for slugs deliberately excluded from publication:

```json
{
  "archived_addons": [
    "zzz_archived_code-server",
    "zzz_archived_jellyseerr",
    "zzz_archived_omada",
    "zzz_archived_omada_v3",
    "zzz_archived_ombi",
    "zzz_archived_overseerr",
    "zzz_archived_paperless_ngx",
    "zzz_archived_papermerge",
    "zzz_archived_plex_meta_manager"
  ]
}
```

The policy module has a small interface: load the archive set, validate that the slugs are unique, and classify a slug as published or archived. `sync-addons.py` consumes this interface before resolving upstream ownership. Archived slugs are never copied to the repository root or inserted into `addons-manifest.json`.

Files are moved with `git mv` from `<slug>/` to `archive/addons/<slug>/`. The Home Assistant repository scanner and this repository's `find_addons()` function only inspect root children containing `config.yaml`, so `archive/` is retained but not published.

## Catalog Health Module

`.claude/scripts/catalog_health.py` owns all derived catalog facts. It exposes a pure `collect_health(root)` function for tests and a CLI:

```text
python .claude/scripts/catalog_health.py --check
python .claude/scripts/catalog_health.py --write-readme
```

`--check` returns nonzero when any invariant fails:

1. manifest add-on keys exactly equal the active root add-on directories;
2. every archived slug is absent from both the active root and manifest, but exists at `archive/addons/<slug>/config.yaml`;
3. every active manifest `zh_guide` value equals the presence of `<!-- zh-guide -->` in its README;
4. README's generated catalog block equals the values derived from the active manifest.

`--write-readme` replaces only the content between `<!-- catalog-stats:start -->` and `<!-- catalog-stats:end -->`. The generated block includes active add-on count, per-source counts, and Chinese-guide count. It fails rather than editing if either marker is missing or appears more than once. This keeps the rest of README hand-authored.

`README.md` displays the generated statistics in the introductory bullets, the Chinese-guide section, FAQ, and source list by referencing one compact generated facts block. Narrative text does not repeat manually maintained counts.

## Docker Baseline Module

`.claude/scripts/check-docker.sh` gains `--baseline <path>`. During an all-repository scan it emits a stable identifier for each failure, `path#line|rule-code`. A baseline file stores the accepted identifiers and a short reason for each legacy class.

The command fails only if it finds a violation absent from the baseline. An identifier no longer emitted is reported as stale but does not fail; removing it from the baseline is part of the change that fixes that add-on. This makes the baseline monotonically shrinkable.

The checker adds two rules:

- `D09`: reject Dockerfile `RUN` instructions that pipe `curl` or `wget` into `sh` or `bash`;
- `D10`: reject Dockerfile `ADD` instructions whose source is an `http://` or `https://` URL.

Existing violations are added to `.claude/baselines/docker-policy.txt`; new occurrences are rejected. The baseline is a governance boundary, not an endorsement of the listed behavior.

## Automation and Failure Handling

`.github/workflows/catalog-quality.yml` runs on pushes and pull requests. It invokes:

```text
python .claude/scripts/catalog_health.py --check
bash .claude/scripts/check-docker.sh --all --baseline .claude/baselines/docker-policy.txt
python -m unittest discover -s tests -p "test_*.py"
```

Each command is deterministic and network-free. The workflow deliberately does not build images or contact upstream registries. Failures identify the invariant, path, and remediation: update generated README statistics with `--write-readme`, move/declare an archived add-on consistently, or add a reviewed baseline entry only for a pre-existing vendored violation.

## Testing

Standard-library `unittest` cases in `tests/test_catalog_health.py` build temporary fixture repositories and cover:

- matching manifest and active directory sets passes;
- a manifest-only slug fails;
- an archived slug at the root or in the manifest fails;
- a missing archive payload fails;
- guide-marker mismatch fails;
- README marker replacement updates only the generated block and rejects missing/duplicate markers.

Shell tests exercise the Docker checker against temporary Dockerfiles: a known baseline identifier passes, a new `curl | bash` and a remote `ADD` fail, and a stale baseline line is reported without masking a new violation.

## Rollout

1. Add tests and the catalog health module.
2. Add policy, move archived payloads, update manifest, and regenerate README.
3. Add Docker rule identifiers and generate the reviewed baseline from the current scan.
4. Add CI and run the full offline verification suite.

The sync exclusion is applied in the ownership-resolution path, so the next `sync-addons.py --dry-run` demonstrates that archived add-ons remain excluded without requiring a network update.
