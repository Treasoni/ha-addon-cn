#!/usr/bin/env bash
set -euo pipefail

check_rule() {
  local fixture="$1" rule="$2" output status
  set +e
  output="$(bash .claude/scripts/check-docker.sh --path "$fixture" 2>&1)"
  status=$?
  set -e

  if [ "$status" -eq 0 ]; then
    echo "expected ${rule} failure for ${fixture}" >&2
    exit 1
  fi
  if ! grep -q "|${rule}:" <<<"$output"; then
    echo "missing ${rule} identifier for ${fixture}" >&2
    printf '%s\n' "$output" >&2
    exit 1
  fi
}

check_rule tests/fixtures/docker-policy/Dockerfile.remote-pipe D09
check_rule tests/fixtures/docker-policy/Dockerfile.remote-add D10
check_rule tests/fixtures/docker-policy/Dockerfile.remote-add-variants D10

fixture_baseline="$(mktemp)"
trap 'rm -f "$fixture_baseline"' EXIT
printf '%s\n' 'tests/fixtures/docker-policy/Dockerfile.remote-pipe#4|D09|fixture baseline' > "$fixture_baseline"

if ! bash .claude/scripts/check-docker.sh --path tests/fixtures/docker-policy/Dockerfile.remote-pipe --baseline "$fixture_baseline" > /dev/null; then
  echo "expected listed fixture violation to pass" >&2
  exit 1
fi

printf '%s\n' 'tests/fixtures/docker-policy/Dockerfile.remote-add#99|D10|stale fixture baseline' >> "$fixture_baseline"
stale_output="$(bash .claude/scripts/check-docker.sh --path tests/fixtures/docker-policy/Dockerfile.remote-pipe --baseline "$fixture_baseline" 2>&1)"
if ! grep -q 'stale baseline: tests/fixtures/docker-policy/Dockerfile.remote-add#99|D10' <<<"$stale_output"; then
  echo "expected stale baseline warning" >&2
  printf '%s\n' "$stale_output" >&2
  exit 1
fi

if bash .claude/scripts/check-docker.sh --path tests/fixtures/docker-policy/Dockerfile.remote-add --baseline "$fixture_baseline" > /dev/null 2>&1; then
  echo "expected unlisted fixture violation to fail" >&2
  exit 1
fi

if ! bash .claude/scripts/check-docker.sh --all --baseline .claude/baselines/docker-policy.txt > /dev/null; then
  echo "expected reviewed Docker policy baseline to pass" >&2
  exit 1
fi
