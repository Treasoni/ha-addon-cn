#!/usr/bin/with-contenv bashio
# shellcheck shell=bash
# actions.sh —— 单一写者动作模块（镜像层 + OTA 层）
# 所有对 docker.json / RAUC 的写操作经 flock 串行化，run.sh 与 server.py 共用。

set -euo pipefail

# ---------------- 基础路径与常量 ----------------
STATE_FILE="${STATE_FILE:-/data/state.json}"
LOCK_FILE="/data/.actions.lock"
BACKUP_LOCAL="/data/docker.json.backup"          # addon_config 本地 last-good 快照
OTA_DIR="/data/ota"                               # addon 内下载目录
HOST_ADDON_DIR="/mnt/data/supervisor/addons_config/${SLUG}"  # HAOS 宿主可见路径（RAUC 需宿主路径）
HOST_OTA_DIR="${HOST_ADDON_DIR}/ota"
SUPERVISOR_URL="http://supervisor"
RESTART_COOLDOWN=900   # 15 分钟重启冷却
PROBE_COOLDOWN=60      # 周期探测至少间隔 60s
AUTO_SWITCH_FAILURE_THRESHOLD=2

# ---------------- 日志 ----------------
_log_info() {
  local msg="$1"
  if declare -F bashio::log.info >/dev/null 2>&1; then
    bashio::log.info "$msg"
  else
    printf '[INFO] %s\n' "$msg"
  fi
}

_log() {
  local msg="$1"
  _log_info "$msg"
  if [ -f "$STATE_FILE" ]; then
    python3 - "$msg" <<'PY' || true
import fcntl, json, os, sys, tempfile, time
try:
    with open("/data/.state.lock", "a+", encoding="utf-8") as lock:
        fcntl.flock(lock.fileno(), fcntl.LOCK_EX)
        try:
            with open("/data/state.json", "r", encoding="utf-8") as f:
                st = json.load(f)
        except Exception:
            st = {}
        log = st.get("log", [])
        log.append({"ts": int(time.time()), "msg": sys.argv[1]})
        st["log"] = log[-50:]
        st["last_action"] = sys.argv[1]
        st["last_action_ts"] = int(time.time())
        fd, tmp = tempfile.mkstemp(prefix="state.", dir="/data")
        try:
            with os.fdopen(fd, "w", encoding="utf-8") as f:
                json.dump(st, f, ensure_ascii=False, indent=2)
                f.flush()
                os.fsync(f.fileno())
            os.replace(tmp, "/data/state.json")
        finally:
            if os.path.exists(tmp):
                os.unlink(tmp)
except Exception:
    pass
PY
  fi
}

# ---------------- 状态文件 ----------------
ensure_state() {
  mkdir -p /data
  python3 - <<'PY'
import fcntl, json, os, tempfile

path = "/data/state.json"
with open("/data/.state.lock", "a+", encoding="utf-8") as lock:
    fcntl.flock(lock.fileno(), fcntl.LOCK_EX)
    try:
        with open(path, encoding="utf-8") as f:
            st = json.load(f)
    except Exception:
        st = {}
    had_onboarding = "onboarding_completed" in st

    defaults = {
        "schema_version": 2,
        "enabled": {"ghcr.io": True, "docker.io": True, "lscr.io": True},
        "active": {},
        "recommended": {},
        "override": {},
        "removed": {},
        "ota": {"downloaded": "", "installed": "", "state": "idle"},
        "probe_results": {},
        "failure_streak": {},
        "proxy_override": [],
        "proxy_removed": [],
        "last_probe_ts": 0,
        "last_restart_ts": 0,
        "last_known_good": None,
        "onboarding_completed": False,
        "last_application": {},
        "last_action": "init",
        "last_action_ts": 0,
        "log": [],
    }
    for key, value in defaults.items():
        if key not in st or (value is not None and not isinstance(st[key], type(value))):
            st[key] = value
    for registry in ("ghcr.io", "docker.io", "lscr.io"):
        st["enabled"].setdefault(registry, True)
    for key, value in defaults["ota"].items():
        st["ota"].setdefault(key, value)
    if st.get("schema_version", 0) < 2:
        st["schema_version"] = 2
    if not had_onboarding and st.get("last_known_good") is not None:
        st["onboarding_completed"] = True

    fd, tmp = tempfile.mkstemp(prefix="state.", dir="/data")
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as f:
            json.dump(st, f, ensure_ascii=False, indent=2)
            f.flush()
            os.fsync(f.fileno())
        os.replace(tmp, path)
    finally:
        if os.path.exists(tmp):
            os.unlink(tmp)
PY
}

_state_field() {
  STATE_FILE="$STATE_FILE" python3 - "$@" <<'PY' || echo ""
import json, sys
import os
try:
    with open(os.environ.get("STATE_FILE", "/data/state.json"), "r", encoding="utf-8") as f:
        st = json.load(f)
except Exception:
    print("")
    sys.exit(0)
keys = sys.argv[1:]
if not keys:
    print("")
    sys.exit(0)
cur = st
for k in keys:
    if not isinstance(cur, dict) or k not in cur:
        print("")
        sys.exit(0)
    cur = cur[k]
if isinstance(cur, bool):
    print("true" if cur else "false")
elif cur is None:
    print("null")
elif isinstance(cur, (dict, list)):
    print(json.dumps(cur, ensure_ascii=False))
else:
    print(cur)
PY
}

_update_state() {
  # _update_state <json-fragment> —— 合并进 state.json
  python3 - "$1" <<'PY'
import fcntl, json, os, sys, tempfile
frag = json.loads(sys.argv[1])
with open("/data/.state.lock", "a+", encoding="utf-8") as lock:
    fcntl.flock(lock.fileno(), fcntl.LOCK_EX)
    with open("/data/state.json", "r", encoding="utf-8") as f:
        st = json.load(f)
    for k, v in frag.items():
        if isinstance(v, dict) and isinstance(st.get(k), dict):
            st[k].update(v)
        else:
            st[k] = v
    fd, tmp = tempfile.mkstemp(prefix="state.", dir="/data")
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as f:
            json.dump(st, f, ensure_ascii=False, indent=2)
            f.flush()
            os.fsync(f.fileno())
        os.replace(tmp, "/data/state.json")
    finally:
        if os.path.exists(tmp):
            os.unlink(tmp)
PY
}

_record_last_known_good() {
  python3 - "$1" <<'PY'
import fcntl, json, os, sys, tempfile
value = json.loads(sys.argv[1])
with open("/data/.state.lock", "a+", encoding="utf-8") as lock:
    fcntl.flock(lock.fileno(), fcntl.LOCK_EX)
    with open("/data/state.json", "r", encoding="utf-8") as f:
        st = json.load(f)
    st["last_known_good"] = value
    fd, tmp = tempfile.mkstemp(prefix="state.", dir="/data")
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as f:
            json.dump(st, f, ensure_ascii=False, indent=2)
            f.flush()
            os.fsync(f.fileno())
        os.replace(tmp, "/data/state.json")
    finally:
        if os.path.exists(tmp):
            os.unlink(tmp)
PY
}

_record_application() {
  local ok="$1"
  local code="$2"
  local requires_restart="$3"
  python3 - "$ok" "$code" "$requires_restart" <<'PY'
import fcntl, json, os, sys, tempfile, time
with open("/data/.state.lock", "a+", encoding="utf-8") as lock:
    fcntl.flock(lock.fileno(), fcntl.LOCK_EX)
    with open("/data/state.json", "r", encoding="utf-8") as f:
        st = json.load(f)
    success = sys.argv[1] == "true"
    st["last_application"] = {
        "ok": success,
        "code": sys.argv[2],
        "requires_restart": sys.argv[3] == "true",
        "ts": int(time.time()),
    }
    if success:
        st["onboarding_completed"] = True
    fd, tmp = tempfile.mkstemp(prefix="state.", dir="/data")
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as f:
            json.dump(st, f, ensure_ascii=False, indent=2)
            f.flush()
            os.fsync(f.fileno())
        os.replace(tmp, "/data/state.json")
    finally:
        if os.path.exists(tmp):
            os.unlink(tmp)
PY
}

# ---------------- Docker 访问 ----------------
docker_cmd() {
  docker "$@"
}

# 读取 hassio_supervisor 容器的 /data/docker.json（HAOS 宿主路径 /mnt/data/supervisor/docker.json）。
docker_read_strict() {
  docker exec hassio_supervisor cat /data/docker.json 2>/dev/null
}

docker_read() {
  docker_read_strict || echo "{}"
}

docker_restore_internal_backup() {
  docker exec hassio_supervisor sh -c 'test -f /data/docker.json.bak && mv -f /data/docker.json.bak /data/docker.json'
}

# 原子写：本地构造 -> jq 校验 -> 备份 -> docker cp -> mv -> 读回复验 -> 失败回滚
docker_write_atomic() {
  local newfile="$1"
  if ! jq -e 'type=="object"' "$newfile" >/dev/null 2>&1; then
    _log "拒绝写入：目标不是合法 JSON 对象（docker_write_atomic）"
    return 1
  fi
  # 容器内备份；没有可靠备份就不能执行任何替换。
  if ! docker exec hassio_supervisor sh -c 'cp -f /data/docker.json /data/docker.json.bak'; then
    _log "无法创建 Supervisor 配置备份，拒绝写入"
    return 1
  fi
  # 本地备份（写入前快照当前生效配置，供「恢复上次配置」）
  if ! docker_read_strict > "$BACKUP_LOCAL"; then
    _log "无法读取 docker.json，拒绝执行旧配置清理"
    return 1
  fi
  # 上传临时文件再 mv（原子替换）
  if ! docker cp "$newfile" hassio_supervisor:/data/docker.json.tmp; then
    _log "docker cp 失败，写回滚"
    docker_restore_internal_backup || _log "旧配置回滚失败"
    return 1
  fi
  if ! docker exec hassio_supervisor sh -c 'mv -f /data/docker.json.tmp /data/docker.json'; then
    _log "容器内 mv 失败，写回滚"
    docker_restore_internal_backup || _log "旧配置回滚失败"
    return 1
  fi
  # 读回复验
  local readback
  if ! readback="$(docker_read_strict)"; then
    _log "写后无法读回 docker.json，回滚备份"
    docker_restore_internal_backup || _log "旧配置回滚失败"
    return 1
  fi
  if ! jq -e 'type=="object"' <<<"$readback" >/dev/null 2>&1; then
    _log "写后复验失败，回滚备份"
    docker_restore_internal_backup || _log "旧配置回滚失败"
    return 1
  fi
  _log "docker.json 写入成功"
  return 0
}

# ---------------- 探测 ----------------
probe_host() {
  local registry="$1"
  local host="$2"
  if ! python3 - "$host" <<'PY'
import re, sys
host = sys.argv[1]
if not re.fullmatch(r"[A-Za-z0-9](?:[A-Za-z0-9.-]{0,251}[A-Za-z0-9])?(?::[0-9]{1,5})?", host):
    raise SystemExit(1)
PY
  then
    echo "fail:invalid_host|0"
    return 0
  fi
  local probe_repo probe_tag
  probe_repo="$(python3 - "$registry" <<'PY'
import json, sys
try:
    with open("/lib/candidates.json", encoding="utf-8") as f:
        spec = json.load(f).get("probe", {}).get(sys.argv[1], {})
    print(spec.get("repository", ""))
except Exception:
    print("")
PY
)"
  probe_tag="$(python3 - "$registry" <<'PY'
import json, sys
try:
    with open("/lib/candidates.json", encoding="utf-8") as f:
        spec = json.load(f).get("probe", {}).get(sys.argv[1], {})
    print(spec.get("tag", ""))
except Exception:
    print("")
PY
)"
  [ -n "$probe_repo" ] && [ -n "$probe_tag" ] || { echo "fail:no_probe_target|0"; return 0; }
  local headers body result code ms content_type
  headers="$(mktemp /tmp/mirror-headers.XXXXXX)"
  body="$(mktemp /tmp/mirror-body.XXXXXX)"
  if ! result="$(curl -sSL -D "$headers" -o "$body" -w "%{http_code}|%{time_total}" \
    -H 'Accept: application/vnd.docker.distribution.manifest.v2+json, application/vnd.oci.image.manifest.v1+json, application/vnd.oci.image.index.v1+json' \
    --connect-timeout "${PROBE_TIMEOUT:-8}" --max-time "${PROBE_TIMEOUT:-8}" \
    "https://${host}/v2/${probe_repo}/manifests/${probe_tag}" 2>/dev/null)"; then
    result="0|0"
  fi
  code="${result%%|*}"
  ms="${result#*|}"
  content_type="$(grep -i '^content-type:' "$headers" 2>/dev/null || true)"
  local manifest_ok=false
  if [ "$code" = "200" ] && printf '%s' "$content_type" | grep -Eqi 'manifest|json'; then
    if python3 - "$body" <<'PY'
import json, sys
try:
    with open(sys.argv[1], encoding="utf-8") as f:
        payload = json.load(f)
except Exception:
    raise SystemExit(1)
if not isinstance(payload, dict) or not any(
    key in payload for key in ("schemaVersion", "mediaType", "manifests", "config", "layers")
):
    raise SystemExit(1)
PY
    then
      manifest_ok=true
    fi
  fi
  rm -f "$headers" "$body"
  if [ "$code" = "401" ]; then
    echo "ok:${code}|${ms}"
  elif [ "$manifest_ok" = "true" ]; then
    echo "ok:${code}|${ms}"
  else
    echo "fail:${code}|${ms}"
  fi
}

_effective_candidates() {
  # _effective_candidates <registry> —— 输出合并后候选列表（内置 + override - removed）
  local reg="$1"
  python3 - "$reg" <<'PY' || true
import json, sys
reg = sys.argv[1]
try:
    with open("/lib/candidates.json", "r", encoding="utf-8") as f:
        builtin = json.load(f).get(reg, [])
    with open("/data/state.json", "r", encoding="utf-8") as f:
        st = json.load(f)
except Exception:
    builtin = []
    st = {}
override = st.get("override", {}).get(reg, [])
removed = set(st.get("removed", {}).get(reg, []))
out = []
for h in list(builtin) + [o for o in override if o not in builtin]:
    if h not in removed and h not in out:
        out.append(h)
print("\n".join(out))
PY
}

_effective_proxies() {
  # 输出有效 gh-proxy 清单（JSON 数组：内置 + state 新增 - state 移除）。
  # 用户增删持久化在 /data/state.json，绝不直接改 /lib/proxy_hosts.json（镜像层，容器重建即丢）。
  python3 - <<'PY' || echo '["ghproxy.net"]'
import json
try:
    with open("/lib/proxy_hosts.json", "r", encoding="utf-8") as f:
        builtin = json.load(f).get("hosts", [])
except Exception:
    builtin = []
try:
    with open("/data/state.json", "r", encoding="utf-8") as f:
        st = json.load(f)
except Exception:
    st = {}
ov = st.get("proxy_override", [])
rm = set(st.get("proxy_removed", []))
out = []
for h in list(builtin) + [o for o in ov if o not in builtin]:
    if h not in rm and h not in out:
        out.append(h)
print(json.dumps(out, ensure_ascii=False))
PY
}

probe_all() {
  # 探测所有启用的 registry，写入推荐源；只有 apply 才会把推荐源提升为 active。
  local reg host code picked fragment
  ensure_state
  {
    for reg in ghcr.io docker.io lscr.io; do
      if [ "$(_state_field enabled "$reg")" != "true" ]; then
        printf 'RECOMMENDED|%s|\n' "$reg"
        continue
      fi
      case "$reg" in
        ghcr.io)   [ "${ENABLE_GHCR:-true}" = "true" ] || { printf 'RECOMMENDED|%s|\n' "$reg"; continue; } ;;
        docker.io) [ "${ENABLE_DOCKERIO:-true}" = "true" ] || { printf 'RECOMMENDED|%s|\n' "$reg"; continue; } ;;
        lscr.io)   [ "${ENABLE_LSCR:-true}" = "true" ] || { printf 'RECOMMENDED|%s|\n' "$reg"; continue; } ;;
      esac
      picked=""
      while IFS= read -r host; do
        [ -n "$host" ] || continue
        code="$(probe_host "$reg" "$host")"
        printf 'RESULT|%s|%s|%s\n' "$reg" "$host" "$code"
        if [[ "$code" == ok:* ]] && [ -z "$picked" ]; then picked="$host"; fi
      done <<< "$(_effective_candidates "$reg")"
      printf 'RECOMMENDED|%s|%s\n' "$reg" "${picked:-}"
    done
    printf 'COMPLETE||\n'
  } | python3 -c '
import json, sys, time
try:
    with open("/data/state.json", encoding="utf-8") as f:
        old = json.load(f)
except Exception:
    old = {}
registries = ("ghcr.io", "docker.io", "lscr.io")
st = {
    "probe_results": {registry: {} for registry in registries},
    "recommended": {},
    "failure_streak": dict(old.get("failure_streak", {})),
    "probe_completed": False,
}
for line in sys.stdin:
    line = line.rstrip("\n")
    if not line:
        continue
    typ, reg, rest = line.split("|", 2)
    if typ == "RESULT":
        host, code = rest.split("|", 1)
        st.setdefault("probe_results", {}).setdefault(reg, {})[host] = code
    elif typ == "RECOMMENDED":
        st.setdefault("recommended", {})[reg] = rest or None
    elif typ == "COMPLETE" and not reg and not rest:
        st["probe_completed"] = True
    else:
        raise ValueError(f"invalid probe record: {line}")
for reg in registries:
    active = old.get("active", {}).get(reg)
    status = st.get("probe_results", {}).get(reg, {}).get(active, "") if active else ""
    if not active or status.startswith("ok:"):
        st.setdefault("failure_streak", {})[reg] = 0
    else:
        st.setdefault("failure_streak", {})[reg] = st.setdefault("failure_streak", {}).get(reg, 0) + 1
st["last_probe_ts"] = int(time.time())
print(json.dumps(st, ensure_ascii=False))
 ' > /data/probe_out.json || true
  fragment="$(cat /data/probe_out.json 2>/dev/null || echo '{}')"
  rm -f /data/probe_out.json
  if ! python3 - "$fragment" <<'PY'
import json, sys

try:
    state = json.loads(sys.argv[1])
except Exception:
    raise SystemExit(1)

# A completed probe may legitimately have no candidates or no successful hosts.
# It is incomplete only when the producer did not finish every registry.
registries = {"ghcr.io", "docker.io", "lscr.io"}
probe_results = state.get("probe_results")
if state.get("probe_completed") is not True:
    raise SystemExit(1)
if not isinstance(probe_results, dict) or set(probe_results) != registries:
    raise SystemExit(1)
if not all(isinstance(results, dict) for results in probe_results.values()):
    raise SystemExit(1)

recommended = state.get("recommended")
if not isinstance(recommended, dict) or set(recommended) != registries:
    raise SystemExit(1)
PY
  then
    _log "镜像源探测失败：无法生成完整探测结果"
    return 1
  fi
  _update_state "$fragment"
  local summary
  summary="$(_probe_summary "$fragment")"
  if python3 - "$fragment" <<'PY'
import json, sys
try:
    recommended = json.loads(sys.argv[1]).get("recommended", {})
except Exception:
    recommended = {}
raise SystemExit(0 if any(recommended.values()) else 1)
PY
  then
    _log "镜像源探测完成：${summary}"
  else
    _log "镜像源检查完成：暂未找到可用候选，已保持当前配置不变：${summary}"
  fi
}

_probe_summary() {
  python3 - "$1" <<'PY'
import json, sys
try:
    state = json.loads(sys.argv[1])
except Exception:
    state = {}
parts = []
for registry in ("ghcr.io", "docker.io", "lscr.io"):
    results = state.get("probe_results", {}).get(registry, {})
    if results:
        detail = ", ".join(f"{host}={status}" for host, status in results.items())
    else:
        detail = "无候选"
    parts.append(f"{registry}[{detail}]")
print("；".join(parts))
PY
}

supervisor_restart() {
  # 重启 Supervisor（会杀掉本 add-on，故 disowned + 延迟；fallback docker restart）
  local now
  now="$(date +%s)"
  _update_state "{\"last_restart_ts\":$now}"
  _log "准备重启 Supervisor…"
  if [ -n "${SUPERVISOR_TOKEN:-}" ]; then
    ( sleep 2; curl -fsS -X POST -H "Authorization: Bearer $SUPERVISOR_TOKEN" \
        "$SUPERVISOR_URL/supervisor/restart" >/dev/null 2>&1 ) >/dev/null 2>&1 &
    disown 2>/dev/null || true
  else
    ( sleep 2; docker restart hassio_supervisor >/dev/null 2>&1 ) >/dev/null 2>&1 &
    disown 2>/dev/null || true
  fi
}

apply() {
  ensure_state
  _log "已拒绝应用镜像映射：HAOS/Supervisor 没有受支持的全局镜像源写入接口"
  _record_application false "MIRROR_APPLICATION_UNSUPPORTED" false
  return 1
}

restore_backup() {
  ensure_state
  _log "已拒绝恢复旧镜像映射：该配置不是 HAOS/Supervisor 支持的接口"
  _record_application false "MIRROR_APPLICATION_UNSUPPORTED" false
  return 1
}

recover_direct() {
  # 仅用于清除旧版本留下的非官方 registries_mirror 字段。
  ensure_state
  local current verify
  if ! current="$(docker_read_strict)"; then
    _log "无法读取 Supervisor 配置，未执行旧配置清理"
    _record_application false "LEGACY_RECOVERY_READ_FAILED" false
    return 1
  fi
  if ! jq -e 'type == "object"' <<<"$current" >/dev/null 2>&1; then
    _log "无法读取 Supervisor 配置，未执行旧配置清理"
    _record_application false "LEGACY_RECOVERY_READ_FAILED" false
    return 1
  fi
  if ! jq -e 'has("registries_mirror")' <<<"$current" >/dev/null 2>&1; then
    _clear_legacy_state
    rm -f "$BACKUP_LOCAL" /data/docker.json.new
    _log "未发现旧版镜像映射，无需清理"
    _record_application true "LEGACY_RECOVERY_NOT_NEEDED" false
    return 0
  fi
  jq 'del(.registries_mirror)' <<<"$current" > /data/docker.json.new
  if ! docker_write_atomic /data/docker.json.new; then
    _log "旧配置清理失败，已尝试回滚"
    _record_application false "LEGACY_RECOVERY_WRITE_FAILED" false
    return 1
  fi
  if ! verify="$(docker_read_strict)"; then
    _log "清理后无法读回 Supervisor 配置，拒绝重启"
    docker_restore_internal_backup || _log "旧配置回滚失败，请不要继续重启 Supervisor"
    _record_application false "LEGACY_RECOVERY_VERIFY_FAILED" false
    return 1
  fi
  if jq -e 'has("registries_mirror")' <<<"$verify" >/dev/null 2>&1; then
    _log "清理后仍检测到 registries_mirror，已回滚且不重启"
    if ! docker_restore_internal_backup; then
      _log "旧配置回滚失败，请不要继续重启 Supervisor"
    fi
    _record_application false "LEGACY_RECOVERY_VERIFY_FAILED" false
    return 1
  fi
  _clear_legacy_state
  rm -f "$BACKUP_LOCAL" /data/docker.json.new
  _log "已清除旧版非官方镜像映射，准备重启 Supervisor"
  _record_application true "LEGACY_MIRROR_REMOVED" true
  supervisor_restart
}

_clear_legacy_state() {
  python3 - <<'PY'
import fcntl, json, os, tempfile
with open("/data/.state.lock", "a+", encoding="utf-8") as lock:
    fcntl.flock(lock.fileno(), fcntl.LOCK_EX)
    with open("/data/state.json", "r", encoding="utf-8") as f:
        st = json.load(f)
    for reg in ("ghcr.io", "docker.io", "lscr.io"):
        st.setdefault("active", {})[reg] = None
    st["recommended"] = {}
    st["last_known_good"] = None
    st["onboarding_completed"] = False
    fd, tmp = tempfile.mkstemp(prefix="state.", dir="/data")
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as f:
            json.dump(st, f, ensure_ascii=False, indent=2)
            f.flush()
            os.fsync(f.fileno())
        os.replace(tmp, "/data/state.json")
    finally:
        if os.path.exists(tmp):
            os.unlink(tmp)
PY
}

# ---------------- 启动检查（只读） ----------------
self_heal() {
  ensure_state
  local current has_mirror
  current="$(docker_read)"
  has_mirror="$(jq -r 'has("registries_mirror")' <<<"$current" 2>/dev/null || echo false)"
  if [ "$has_mirror" = "true" ]; then
    _log "检测到旧版非官方镜像映射；不会自动改写，请在 Web 界面选择「清除旧配置并恢复直连」"
  else
    _log "未检测到旧版镜像映射；启动检查为只读，不会修改 Supervisor 配置"
  fi
  return 0
}

auto_switch_cycle() {
  ensure_state
  local now last_probe last_restart onboarding
  now="$(date +%s)"
  last_probe="$(_state_field last_probe_ts)"
  last_restart="$(_state_field last_restart_ts)"
  onboarding="$(_state_field onboarding_completed)"
  if [ "$onboarding" != "true" ]; then
    _log "首次引导尚未确认，自动换源只探测不应用"
    probe_all || return 1
    return 0
  fi
  [ -n "$last_probe" ] && [ "$(( now - last_probe ))" -lt "$PROBE_COOLDOWN" ] && return 0
  [ -n "$last_restart" ] && [ "$(( now - last_restart ))" -lt "$RESTART_COOLDOWN" ] && {
    _log "重启冷却期内，跳过自动换源"
    return 0
  }
  probe_all || { _log "镜像源探测失败，跳过本次自动换源"; return 1; }
  _log "自动维护已完成只读检查；不会自动切换或重启 Supervisor"
  return 0
}

# ---------------- OTA 层 ----------------
ota_check() {
  # 读 /os/info 的当前版本与最新版本
  ensure_state
  [ "${ENABLE_OTA:-false}" = "true" ] || { _log "OTA 实验功能未启用"; return 1; }
  local info cur latest board
  info="$(curl -fsS -H "Authorization: Bearer $SUPERVISOR_TOKEN" "$SUPERVISOR_URL/os/info" 2>/dev/null || echo "{}")"
  cur="$(jq -r '.data.version // "unknown"' <<<"$info" 2>/dev/null)"
  latest="$(jq -r '.data.version_latest // .data.latest_version // "unknown"' <<<"$info" 2>/dev/null)"
  board="$(jq -r '.data.board // ""' <<<"$info" 2>/dev/null)"
  python3 - "$cur" "$latest" "$board" <<'PY' || true
import json, sys
try:
    with open("/data/state.json", "r", encoding="utf-8") as f:
        st = json.load(f)
except Exception:
    st = {}
st["ota"] = st.get("ota", {})
st["ota"]["current_version"] = sys.argv[1]
st["ota"]["latest_version"] = sys.argv[2]
if sys.argv[3]:
    st["ota"]["board"] = sys.argv[3]
with open("/data/state.json", "w", encoding="utf-8") as f:
    json.dump(st, f, ensure_ascii=False, indent=2)
PY
  _log "OTA 检查：当前=${cur}，最新=${latest}"
  [ "$cur" != "unknown" ] && [ "$latest" != "unknown" ] && [ "$cur" != "$latest" ]
}

_os_board() {
  _state_field ota board
}

ota_download() {
  # ota_download <version>
  ensure_state
  local version="$1"
  local board target ok=false
  [ "${ENABLE_OTA:-false}" = "true" ] || { _log "OTA 实验功能未启用"; return 1; }
  board="$(_state_field ota board)"
  [ -n "$board" ] && [ "$board" != "null" ] || { _log "OTA 下载失败：Supervisor 未返回有效 board"; return 1; }
  mkdir -p "$OTA_DIR"
  _log "OTA 下载：haos_${board}-${version}.raucb"
  local hosts
  hosts="$(_effective_proxies)"
  python3 - "$hosts" "$board" "$version" <<'PY' > /tmp/ota_urls.txt || true
import json, sys
try:
    hosts = json.loads(sys.argv[1])
except Exception:
    hosts = ["ghproxy.net"]
board, version = sys.argv[2], sys.argv[3]
gh = "https://github.com/home-assistant/operating-system/releases/download/{v}/haos_{b}-{v}.raucb".format(v=version, b=board)
for h in hosts:
    print("https://{0}/{1}".format(h, gh))
PY
  while IFS= read -r url; do
    [ -n "$url" ] || continue
    _log_info "尝试下载源：$url"
    if curl -sSfL --retry 2 --retry-delay 3 --max-time 600 -C - \
        -o "$OTA_DIR/haos_${board}-${version}.raucb" "$url"; then
      if [ -s "$OTA_DIR/haos_${board}-${version}.raucb" ]; then
        ok=true
        break
      fi
    fi
  done < /tmp/ota_urls.txt
  rm -f /tmp/ota_urls.txt
  if [ "$ok" = "true" ]; then
    local size
    size="$(stat -c %s "$OTA_DIR/haos_${board}-${version}.raucb" 2>/dev/null || echo 0)"
    _log "OTA 下载完成：${size} 字节（宿主路径 ${HOST_OTA_DIR}/haos_${board}-${version}.raucb）"
    _update_state "{\"ota\":{\"downloaded\":\"haos_${board}-${version}.raucb\",\"downloaded_board\":\"${board}\",\"downloaded_version\":\"${version}\",\"state\":\"downloaded\"}}"
    return 0
  fi
  _log "OTA 下载失败：全部 gh-proxy 源不可用（可在 Web 界面增删代理清单）"
  _update_state "{\"ota\":{\"state\":\"download_failed\"}}"
  return 1
}

ota_install() {
  # 经 host_dbus 调 RAUC D-Bus Installer.Install（宿主路径）
  ensure_state
  [ "${ENABLE_OTA:-false}" = "true" ] || { _log "OTA 实验功能未启用"; return 1; }
  local board ver fname target
  board="$(_state_field ota downloaded_board)"
  ver="$(_state_field ota downloaded_version)"
  fname="$(_state_field ota downloaded)"
  if [ -z "$board" ] || [ -z "$ver" ] || [ -z "$fname" ] || [ "$fname" = "null" ]; then
    _log "OTA 安装：没有已下载的升级包，先下载"
    return 1
  fi
  target="${HOST_OTA_DIR}/${fname}"
  if [ ! -s "/data/ota/${fname}" ]; then
    _log "OTA 安装：升级包不存在或为空（$target）"
    return 1
  fi
  _log "OTA 安装：调用 RAUC Installer.Install（$target）"
  if dbus-send --system --print-reply --dest=de.pengutronix.rauc \
      / de.pengutronix.rauc.Installer.Install "string:${target}"; then
    _log "OTA 安装已提交（RAUC 后台执行，验签由宿主 keyring 完成）"
    _update_state "{\"ota\":{\"installed\":\"${fname}\",\"state\":\"installed\"}}"
    return 0
  fi
  _log "OTA 安装提交失败"
  _update_state "{\"ota\":{\"state\":\"install_failed\"}}"
  return 1
}

ota_reboot() {
  # POST /host/reboot —— 服务器返回前宿主已重启
  ensure_state
  [ "${ENABLE_OTA:-false}" = "true" ] || { _log "OTA 实验功能未启用"; return 1; }
  _log "重启宿主以生效 OTA 更新…"
  curl -fsS -X POST -H "Authorization: Bearer $SUPERVISOR_TOKEN" \
      "$SUPERVISOR_URL/host/reboot" >/dev/null 2>&1 || true
}
