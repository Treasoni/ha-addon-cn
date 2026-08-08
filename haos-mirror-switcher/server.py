#!/usr/bin/env python3
"""haos-mirror-switcher ingress API.

The API intentionally exposes a small, user-facing result contract while keeping
technical command output in the add-on log.
"""

import fcntl
import json
import os
import re
import subprocess
import tempfile
import threading
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

STATE_FILE = "/data/state.json"
CANDIDATES_FILE = "/lib/candidates.json"
PROXY_FILE = "/lib/proxy_hosts.json"
INGRESS_PORT = int(os.environ.get("INGRESS_PORT", "8569"))
SLUG = os.environ.get("SLUG", "haos-mirror-switcher")
REGISTRIES = ("ghcr.io", "docker.io", "lscr.io")
HOST_RE = re.compile(r"^[A-Za-z0-9](?:[A-Za-z0-9.-]{0,251}[A-Za-z0-9])?(?::[0-9]{1,5})?$")
VERSION_RE = re.compile(r"^[0-9][0-9A-Za-z._-]*$")
_lock = threading.Lock()


def sh(*args):
    """Call a fixed actions.sh function without shell-string interpolation."""
    if not args or args[0] not in {
        "probe_all",
        "apply",
        "restore_backup",
        "supervisor_restart",
        "recover_direct",
        "ota_check",
        "ota_download",
        "ota_install",
        "ota_reboot",
    }:
        return False, "", "unsupported action"
    cmd = ["bash", "-c", 'source /lib/actions.sh; "$@"', "actions.sh", *args]
    env = dict(os.environ)
    env["PROBE_TIMEOUT"] = os.environ.get("PROBE_TIMEOUT", "8")
    env["SLUG"] = SLUG
    try:
        proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, env=env)
        output, error = proc.communicate(timeout=900)
    except subprocess.TimeoutExpired:
        proc.kill()
        output, error = proc.communicate()
        print(f"[action:{args[0]}:stderr] timeout", flush=True)
        return False, "", "timeout"
    output = output.decode("utf-8", errors="replace").strip()
    error = error.decode("utf-8", errors="replace").strip()
    for stream, content in (("stdout", output), ("stderr", error)):
        for line in content.splitlines():
            print(f"[action:{args[0]}:{stream}] {line}", flush=True)
    return proc.returncode == 0, output, error


def load_state():
    try:
        with open(STATE_FILE, "r", encoding="utf-8") as file:
            return json.load(file)
    except Exception:
        return {}


def write_state(state):
    os.makedirs(os.path.dirname(STATE_FILE), exist_ok=True)
    with open("/data/.state.lock", "a+", encoding="utf-8") as lock_file:
        fcntl.flock(lock_file.fileno(), fcntl.LOCK_EX)
        fd, temp_path = tempfile.mkstemp(prefix="state.", dir="/data")
        try:
            with os.fdopen(fd, "w", encoding="utf-8") as file:
                json.dump(state, file, ensure_ascii=False, indent=2)
                file.flush()
                os.fsync(file.fileno())
            os.replace(temp_path, STATE_FILE)
        finally:
            if os.path.exists(temp_path):
                os.unlink(temp_path)


def read_docker_mirror():
    try:
        proc = subprocess.run(
            ["docker", "exec", "hassio_supervisor", "cat", "/data/docker.json"],
            capture_output=True,
            text=True,
            timeout=15,
        )
        return json.loads(proc.stdout).get("registries_mirror", {})
    except Exception:
        return {}


def socket_available():
    return os.path.exists("/var/run/docker.sock") or os.path.exists("/run/docker.sock")


def read_candidates():
    try:
        with open(CANDIDATES_FILE, "r", encoding="utf-8") as file:
            raw = json.load(file)
        return {registry: raw.get(registry, []) for registry in REGISTRIES}
    except Exception:
        return {registry: [] for registry in REGISTRIES}


def read_proxies():
    try:
        with open(PROXY_FILE, "r", encoding="utf-8") as file:
            builtin = json.load(file).get("hosts", [])
    except Exception:
        builtin = []
    state = load_state()
    overrides = state.get("proxy_override", [])
    removed = set(state.get("proxy_removed", []))
    return [
        host
        for host in list(builtin) + [host for host in overrides if host not in builtin]
        if host not in removed
    ]


def ota_enabled():
    return os.environ.get("ENABLE_OTA", "false") == "true"


def valid_host(value):
    if not isinstance(value, str) or not HOST_RE.fullmatch(value):
        return False
    hostname = value
    port = None
    if ":" in value:
        hostname, port_text = value.rsplit(":", 1)
        try:
            port = int(port_text)
        except ValueError:
            return False
        if not 1 <= port <= 65535:
            return False
    labels = hostname.split(".")
    if any(not label or len(label) > 63 for label in labels):
        return False
    if any(label.startswith("-") or label.endswith("-") for label in labels):
        return False
    return len(hostname) <= 253


def result(ok, code, user_message, *, retryable=False, requires_restart=False, **extra):
    payload = {
        "ok": ok,
        "code": code,
        "user_message": user_message,
        "retryable": retryable,
        "requires_restart": requires_restart,
    }
    payload.update(extra)
    return payload


class Handler(BaseHTTPRequestHandler):
    def log_message(self, *_args):
        return

    def _send_json(self, payload, code=200):
        body = json.dumps(payload, ensure_ascii=False).encode("utf-8")
        self.send_response(code)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def _read_body(self):
        try:
            length = int(self.headers.get("Content-Length", 0))
            return json.loads(self.rfile.read(length).decode("utf-8")) if length else {}
        except Exception:
            return {}

    def _action(self, fn, ok_code, ok_message, fail_code, fail_message, *, restart=False):
        success, output, error = sh(fn)
        state = load_state()
        application = (
            state.get("last_application", {})
            if fn in {"apply", "restore_backup", "recover_direct"}
            else {}
        )
        if success:
            if fn == "probe_all" and not any(state.get("recommended", {}).values()):
                return result(
                    True,
                    "PROBE_COMPLETED_NO_RECOMMENDATION",
                    "检查完成，但暂未找到可用的镜像源；当前配置没有改动。",
                    retryable=True,
                    requires_restart=False,
                    details=output,
                )
            actual_code = application.get("code", ok_code)
            actual_restart = bool(application.get("requires_restart", restart))
            if actual_code == "LEGACY_RECOVERY_NOT_NEEDED":
                return result(
                    True,
                    actual_code,
                    "未发现旧版镜像映射，无需清理或重启 Supervisor",
                    retryable=False,
                    requires_restart=False,
                    details=output,
                )
            return result(
                True,
                actual_code,
                "配置未变化，无需重启 Supervisor" if actual_code == "APPLIED_NO_CHANGE" else ok_message,
                retryable=False,
                requires_restart=actual_restart,
                details=output,
            )
        actual_fail_code = application.get("code", fail_code)
        if actual_fail_code == "MIRROR_APPLICATION_UNSUPPORTED":
            return result(
                False,
                actual_fail_code,
                "此版本不会修改 Supervisor 镜像配置；请使用真实的 Docker/HAOS 网络配置",
                retryable=False,
                requires_restart=False,
                details=error or output,
            )
        return result(
            False,
            actual_fail_code,
            fail_message,
            retryable=True,
            requires_restart=False,
            details=error or output,
        )

    def do_GET(self):
        if self.path in ("/", "/index.html"):
            try:
                with open("/www/index.html", "r", encoding="utf-8") as file:
                    body = file.read().encode("utf-8")
                self.send_response(200)
                self.send_header("Content-Type", "text/html; charset=utf-8")
                self.send_header("Content-Length", str(len(body)))
                self.end_headers()
                self.wfile.write(body)
            except Exception:
                self._send_json(result(False, "UI_NOT_FOUND", "界面文件缺失"), 500)
            return

        if self.path == "/api/status":
            state = load_state()
            ota = state.get("ota", {})
            current_mirror = read_docker_mirror()
            self._send_json({
                    **result(True, "STATUS_OK", "状态读取成功"),
                    "slug": SLUG,
                    "socket": socket_available(),
                    "current_mirror": current_mirror,
                    "legacy_mirror_detected": bool(current_mirror),
                    "active": state.get("active", {}),
                    "recommended": state.get("recommended", {}),
                    "enabled": state.get("enabled", {}),
                    "override": state.get("override", {}),
                    "removed": state.get("removed", {}),
                    "probe_results": state.get("probe_results", {}),
                    "failure_streak": state.get("failure_streak", {}),
                    "candidates": read_candidates(),
                    "proxies": read_proxies(),
                    "ota": ota,
                    "ota_enabled": ota_enabled(),
                    "onboarding_pending": not bool(state.get("onboarding_completed")),
                    "onboarding_completed": bool(state.get("onboarding_completed")),
                    "last_application": state.get("last_application", {}),
                    "last_probe_ts": state.get("last_probe_ts"),
                    "last_restart_ts": state.get("last_restart_ts"),
                    "last_action": state.get("last_action"),
                    "last_action_ts": state.get("last_action_ts"),
                    "log": state.get("log", [])[-30:],
                    "options": {
                        "auto_switch": os.environ.get("AUTO_SWITCH", "true"),
                        "probe_interval_hours": os.environ.get("PROBE_INTERVAL_HOURS", "6"),
                        "probe_timeout_seconds": os.environ.get("PROBE_TIMEOUT", "8"),
                        "enable_ota": os.environ.get("ENABLE_OTA", "false"),
                    },
                })
            return

        self._send_json(result(False, "NOT_FOUND", "请求不存在"), 404)

    def do_POST(self):
        if self.path == "/api/probe":
            with _lock:
                return self._send_json(
                    self._action(
                        "probe_all",
                        "PROBE_COMPLETED",
                        "检查完成，请确认推荐镜像源后应用",
                        "PROBE_FAILED",
                        "镜像源检查失败，请稍后重试",
                    )
                )

        if self.path == "/api/apply":
            with _lock:
                return self._send_json(
                    self._action(
                        "apply",
                        "APPLIED",
                        "配置已应用，Supervisor 正在重启，稍后刷新页面",
                        "APPLY_FAILED",
                        "配置应用失败，原配置已保留或已回滚",
                        restart=True,
                    )
                )

        if self.path == "/api/restore":
            with _lock:
                return self._send_json(
                    self._action(
                        "restore_backup",
                        "RESTORED",
                        "已恢复上次配置，Supervisor 正在重启",
                        "RESTORE_FAILED",
                        "恢复上次配置失败",
                        restart=True,
                    )
                )

        if self.path == "/api/restart-supervisor":
            with _lock:
                return self._send_json(
                    self._action(
                        "supervisor_restart",
                        "SUPERVISOR_RESTARTING",
                        "Supervisor 正在重启，加载项会短暂离线",
                        "SUPERVISOR_RESTART_FAILED",
                        "Supervisor 重启请求失败",
                        restart=True,
                    )
                )

        if self.path == "/api/recover-direct":
            with _lock:
                return self._send_json(
                    self._action(
                        "recover_direct",
                        "DIRECT_RESTORED",
                        "已移除镜像映射，Supervisor 正在重启",
                        "DIRECT_RESTORE_FAILED",
                        "恢复直连失败",
                        restart=True,
                    )
                )

        if self.path == "/api/toggle":
            body = self._read_body()
            registry = body.get("registry")
            if registry not in REGISTRIES or not isinstance(body.get("enabled"), bool):
                return self._send_json(result(False, "INVALID_REGISTRY", "仓库参数不合法"), 400)
            with _lock:
                state = load_state()
                state.setdefault("enabled", {})[registry] = body["enabled"]
                write_state(state)
            return self._send_json(result(True, "TOGGLE_SAVED", "高级设置已保存"))

        if self.path == "/api/candidates":
            body = self._read_body()
            registry = body.get("registry")
            host = body.get("host", "")
            action = body.get("action")
            if registry not in REGISTRIES or not valid_host(host) or action not in ("add", "remove"):
                return self._send_json(result(False, "INVALID_CANDIDATE", "镜像源主机名不合法"), 400)
            with _lock:
                self._mutate_candidates(registry, host, action)
            return self._send_json(result(True, "CANDIDATE_SAVED", "候选镜像源已保存"))

        if self.path == "/api/proxy-hosts":
            body = self._read_body()
            host = body.get("host", "")
            action = body.get("action")
            if not valid_host(host) or action not in ("add", "remove"):
                return self._send_json(result(False, "INVALID_PROXY", "下载代理主机名不合法"), 400)
            with _lock:
                self._mutate_proxies(host, action)
            return self._send_json(result(True, "PROXY_SAVED", "下载代理已保存"))

        if self.path.startswith("/api/ota/") and not ota_enabled():
            return self._send_json(result(False, "OTA_DISABLED", "OTA 实验功能当前未启用"), 403)

        if self.path == "/api/ota/check":
            with _lock:
                return self._send_json(
                    self._action(
                        "ota_check",
                        "OTA_CHECKED",
                        "OTA 版本检查完成",
                        "OTA_CHECK_FAILED",
                        "OTA 检查失败，不影响镜像换源功能",
                    )
                )

        if self.path == "/api/ota/download":
            with _lock:
                body = self._read_body()
                version = body.get("version", "") or load_state().get("ota", {}).get("latest_version", "")
                if not VERSION_RE.fullmatch(version):
                    return self._send_json(result(False, "INVALID_VERSION", "版本号格式不合法"), 400)
                success, output, error = sh("ota_download", version)
                return self._send_json(
                    result(
                        success,
                        "OTA_DOWNLOADED" if success else "OTA_DOWNLOAD_FAILED",
                        "升级包下载完成，可以安装到备用槽位" if success else "升级包下载失败；可稍后重试或更换高级代理",
                        retryable=not success,
                        details=output or error,
                    )
                )

        if self.path == "/api/ota/install":
            with _lock:
                return self._send_json(
                    self._action(
                        "ota_install",
                        "OTA_INSTALLED",
                        "升级包已安装到备用槽位，需重启系统生效",
                        "OTA_INSTALL_FAILED",
                        "OTA 安装失败，系统未重启",
                    )
                )

        if self.path == "/api/ota/reboot":
            with _lock:
                return self._send_json(
                    self._action(
                        "ota_reboot",
                        "OTA_REBOOTING",
                        "系统正在重启，约 1-2 分钟后恢复",
                        "OTA_REBOOT_FAILED",
                        "系统重启请求失败",
                        restart=True,
                    )
                )

        self._send_json(result(False, "NOT_FOUND", "请求不存在"), 404)

    @staticmethod
    def _mutate_candidates(registry, host, action):
        state = load_state()
        state.setdefault("override", {}).setdefault(registry, [])
        state.setdefault("removed", {}).setdefault(registry, [])
        if action == "add":
            if host not in state["override"][registry]:
                state["override"][registry].append(host)
            if host in state["removed"][registry]:
                state["removed"][registry].remove(host)
        else:
            if host in state["override"][registry]:
                state["override"][registry].remove(host)
            if host not in state["removed"][registry]:
                state["removed"][registry].append(host)
        write_state(state)

    @staticmethod
    def _mutate_proxies(host, action):
        state = load_state()
        state.setdefault("proxy_override", [])
        state.setdefault("proxy_removed", [])
        if action == "add":
            if host not in state["proxy_override"]:
                state["proxy_override"].append(host)
            if host in state["proxy_removed"]:
                state["proxy_removed"].remove(host)
        else:
            if host in state["proxy_override"]:
                state["proxy_override"].remove(host)
            if host not in state["proxy_removed"]:
                state["proxy_removed"].append(host)
        write_state(state)


if __name__ == "__main__":
    print(f"haos-mirror-switcher web ui listening on {INGRESS_PORT}", flush=True)
    server = ThreadingHTTPServer(("0.0.0.0", INGRESS_PORT), Handler)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
