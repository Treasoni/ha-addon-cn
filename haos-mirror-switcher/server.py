#!/usr/bin/env python3
# server.py —— haos-mirror-switcher 内嵌 ingress Web 界面（纯 stdlib，无第三方依赖）
# 只经 Supervisor ingress 进入（已登录鉴权），故无需 CSRF。
# 所有写操作经 lib/actions.sh（flock 串行化）。

import json
import os
import re
import subprocess
import threading
import time
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

STATE_FILE = "/data/state.json"
CANDIDATES_FILE = "/lib/candidates.json"
PROXY_FILE = "/lib/proxy_hosts.json"
INGRESS_PORT = int(os.environ.get("INGRESS_PORT", "8569"))
SLUG = os.environ.get("SLUG", "haos-mirror-switcher")

_lock = threading.Lock()


def sh(*args):
    """调用 actions.sh 函数（bash 环境）。"""
    fn = args[0]
    rest = args[1:]
    cmd = ["bash", "-c", f"source /lib/actions.sh; {fn} " + " ".join(rest)]
    env = dict(os.environ)
    env["PROBE_TIMEOUT"] = os.environ.get("PROBE_TIMEOUT", "8")
    env["SLUG"] = SLUG
    try:
        proc = subprocess.run(cmd, capture_output=True, text=True, timeout=900, env=env)
        return proc.returncode == 0, proc.stdout.strip(), proc.stderr.strip()
    except subprocess.TimeoutExpired:
        return False, "", "timeout"


def load_state():
    try:
        with open(STATE_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return {}


def read_docker_mirror():
    """读当前 docker.json 的 registries_mirror（经 supervisor 容器）。"""
    try:
        out = subprocess.run(
            ["docker", "exec", "hassio_supervisor", "cat", "/data/docker.json"],
            capture_output=True, text=True, timeout=15,
        ).stdout
        return json.loads(out).get("registries_mirror", {})
    except Exception:
        return {}


def socket_available():
    return os.path.exists("/var/run/docker.sock") or os.path.exists("/run/docker.sock")


def read_candidates():
    try:
        with open(CANDIDATES_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return {}


def read_proxies():
    """有效 gh-proxy 清单（内置 + state 新增 - state 移除；增删持久化在 /data/state.json，
    不直接改 /lib/proxy_hosts.json —— 那是镜像层，容器重建即丢）。"""
    try:
        with open(PROXY_FILE, "r", encoding="utf-8") as f:
            builtin = json.load(f).get("hosts", [])
    except Exception:
        builtin = []
    st = load_state()
    ov = st.get("proxy_override", [])
    rm = set(st.get("proxy_removed", []))
    out = []
    for h in list(builtin) + [o for o in ov if o not in builtin]:
        if h not in rm and h not in out:
            out.append(h)
    return out


class Handler(BaseHTTPRequestHandler):
    def log_message(self, *args):
        pass

    def _send_json(self, obj, code=200):
        body = json.dumps(obj, ensure_ascii=False).encode("utf-8")
        self.send_response(code)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def _read_body(self):
        try:
            n = int(self.headers.get("Content-Length", 0))
            return json.loads(self.rfile.read(n).decode("utf-8")) if n else {}
        except Exception:
            return {}

    def do_GET(self):
        if self.path in ("/", "/index.html"):
            try:
                with open("/www/index.html", "r", encoding="utf-8") as f:
                    body = f.read().encode("utf-8")
                self.send_response(200)
                self.send_header("Content-Type", "text/html; charset=utf-8")
                self.send_header("Content-Length", str(len(body)))
                self.end_headers()
                self.wfile.write(body)
                return
            except Exception:
                self._send_json({"error": "index not found"}, 500)
                return
        if self.path == "/api/status":
            st = load_state()
            self._send_json({
                "slug": SLUG,
                "socket": socket_available(),
                "current_mirror": read_docker_mirror(),
                "active": st.get("active", {}),
                "enabled": st.get("enabled", {}),
                "override": st.get("override", {}),
                "removed": st.get("removed", {}),
                "candidates": read_candidates(),
                "proxies": read_proxies(),
                "ota": st.get("ota", {}),
                "last_probe_ts": st.get("last_probe_ts"),
                "last_restart_ts": st.get("last_restart_ts"),
                "last_action": st.get("last_action"),
                "last_action_ts": st.get("last_action_ts"),
                "log": st.get("log", [])[-30:],
                "options": {
                    "auto_switch": os.environ.get("AUTO_SWITCH", "true"),
                    "probe_interval_hours": os.environ.get("PROBE_INTERVAL_HOURS", "6"),
                    "probe_timeout_seconds": os.environ.get("PROBE_TIMEOUT", "8"),
                    "enable_ota": os.environ.get("ENABLE_OTA", "true"),
                },
            })
            return
        self._send_json({"error": "not found"}, 404)

    def do_POST(self):
        if self.path == "/api/probe":
            with _lock:
                ok, out, err = sh("probe_all")
            self._send_json({"ok": ok, "out": out, "err": err})
            return
        if self.path == "/api/apply":
            with _lock:
                ok, out, err = sh("apply")
            self._send_json({"ok": ok, "out": out, "err": err,
                             "note": "配置已写入，正在重启 Supervisor，加载项将自动恢复，请稍候刷新"})
            return
        if self.path == "/api/restore":
            with _lock:
                ok, out, err = sh("restore_backup")
            self._send_json({"ok": ok, "out": out, "err": err,
                             "note": "已恢复上次配置并重启 Supervisor"})
            return
        if self.path == "/api/restart-supervisor":
            with _lock:
                ok, out, err = sh("supervisor_restart")
            self._send_json({"ok": True, "out": out, "err": err,
                             "note": "正在重启 Supervisor，加载项将短暂离线"})
            return
        if self.path == "/api/recover-direct":
            with _lock:
                ok, out, err = sh("recover_direct")
            self._send_json({"ok": ok, "out": out, "err": err,
                             "note": "已恢复直连（移除镜像映射）并重启 Supervisor"})
            return
        if self.path == "/api/toggle":
            body = self._read_body()
            reg = body.get("registry")
            enabled = bool(body.get("enabled"))
            with _lock:
                self._toggle(reg, enabled)
            self._send_json({"ok": True})
            return
        if self.path == "/api/candidates":
            body = self._read_body()
            reg = body.get("registry")
            host = body.get("host")
            action = body.get("action")
            if not reg or not host or action not in ("add", "remove"):
                self._send_json({"ok": False, "error": "need registry/host/action"}, 400)
                return
            with _lock:
                self._mutate_candidates(reg, host, action)
            self._send_json({"ok": True})
            return
        if self.path == "/api/proxy-hosts":
            body = self._read_body()
            host = body.get("host")
            action = body.get("action")
            if not host or action not in ("add", "remove"):
                self._send_json({"ok": False, "error": "need host/action"}, 400)
                return
            with _lock:
                self._mutate_proxies(host, action)
            self._send_json({"ok": True})
            return
        if self.path == "/api/ota/check":
            ok, out, err = sh("ota_check")
            self._send_json({"ok": ok, "out": out, "err": err})
            return
        if self.path == "/api/ota/download":
            body = self._read_body()
            ver = body.get("version", "") or load_state().get("ota", {}).get("latest_version", "")
            if ver and not re.fullmatch(r"[0-9][0-9A-Za-z._-]*", ver):
                self._send_json({"ok": False, "error": "版本号格式不合法"}, 400)
                return
            with _lock:
                ok, out, err = sh("ota_download", ver) if ver else (False, "", "缺少版本号")
            self._send_json({"ok": ok, "out": out, "err": err})
            return
        if self.path == "/api/ota/install":
            with _lock:
                ok, out, err = sh("ota_install")
            self._send_json({"ok": ok, "out": out, "err": err,
                             "note": "升级包已安装到备用槽位，需要重启系统才能生效"})
            return
        if self.path == "/api/ota/reboot":
            with _lock:
                ok, out, err = sh("ota_reboot")
            self._send_json({"ok": True, "out": out, "err": err,
                             "note": "正在重启系统，约 1-2 分钟后自动恢复，请稍候刷新"})
            return
        self._send_json({"error": "not found"}, 404)

    def _toggle(self, reg, enabled):
        st = load_state()
        st.setdefault("enabled", {})[reg] = enabled
        self._write_state(st)

    def _mutate_candidates(self, reg, host, action):
        st = load_state()
        st.setdefault("override", {}).setdefault(reg, [])
        st.setdefault("removed", {}).setdefault(reg, [])
        if action == "add":
            if host not in st["override"][reg]:
                st["override"][reg].append(host)
            if host in st["removed"][reg]:
                st["removed"][reg].remove(host)
        else:  # remove
            # 内置候选也记入 removed；override 里的直接删除
            if host in st["override"][reg]:
                st["override"][reg].remove(host)
            if host not in st["removed"][reg]:
                st["removed"][reg].append(host)
        self._write_state(st)

    def _mutate_proxies(self, host, action):
        # 写入 state（/data 持久化），绝不直接改 /lib/proxy_hosts.json（镜像层，容器重建即丢）
        st = load_state()
        st.setdefault("proxy_override", [])
        st.setdefault("proxy_removed", [])
        if action == "add":
            if host not in st["proxy_override"]:
                st["proxy_override"].append(host)
            if host in st["proxy_removed"]:
                st["proxy_removed"].remove(host)
        else:  # remove
            if host in st["proxy_override"]:
                st["proxy_override"].remove(host)
            if host not in st["proxy_removed"]:
                st["proxy_removed"].append(host)
        self._write_state(st)

    def _write_state(self, st):
        with open(STATE_FILE, "w", encoding="utf-8") as f:
            json.dump(st, f, ensure_ascii=False, indent=2)


if __name__ == "__main__":
    print(f"haos-mirror-switcher web ui listening on {INGRESS_PORT}", flush=True)
    server = ThreadingHTTPServer(("0.0.0.0", INGRESS_PORT), Handler)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
