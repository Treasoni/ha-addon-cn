import contextlib
import importlib.util
import io
import json
import os
import re
import subprocess
import sys
import tempfile
import types
import unittest
from pathlib import Path
from unittest import mock


ROOT = Path(__file__).resolve().parents[1]
ACTIONS = ROOT / "haos-mirror-switcher" / "lib" / "actions.sh"
SERVER = ROOT / "haos-mirror-switcher" / "server.py"
CONFIG = ROOT / "haos-mirror-switcher" / "config.yaml"
CANDIDATES = ROOT / "haos-mirror-switcher" / "lib" / "candidates.json"
UI = ROOT / "haos-mirror-switcher" / "www" / "index.html"


def shell_function_body(name):
    """Return one top-level bash function body for narrow safety assertions."""
    source = ACTIONS.read_text(encoding="utf-8")
    match = re.search(rf"^{re.escape(name)}\(\) \{{(?P<body>.*?)^\}}", source, re.MULTILINE | re.DOTALL)
    if match is None:
        raise AssertionError(f"missing shell function: {name}")
    return match.group("body")


@contextlib.contextmanager
def bash_env_with_python3():
    """Provide a usable python3 command when exercising add-on shell code on Windows."""
    env = os.environ.copy()
    probe = subprocess.run(
        ["bash", "-c", "python3 -c 'import sys'"],
        capture_output=True,
        env=env,
        timeout=10,
    )
    if probe.returncode == 0:
        yield env
        return

    with tempfile.TemporaryDirectory() as temp_dir:
        shim = Path(temp_dir) / "python3"
        shim.write_text('#!/usr/bin/env bash\nexec python "$@"\n', encoding="utf-8")
        shim.chmod(0o755)
        env["PATH"] = f"{temp_dir}{os.pathsep}{env.get('PATH', '')}"
        yield env


def load_server_module():
    try:
        __import__("fcntl")
    except ModuleNotFoundError:
        fake_fcntl = types.ModuleType("fcntl")
        fake_fcntl.LOCK_EX = 2
        fake_fcntl.flock = lambda *_args: None
        sys.modules["fcntl"] = fake_fcntl
    spec = importlib.util.spec_from_file_location("haos_mirror_switcher_server", SERVER)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class HaosMirrorSwitcherTests(unittest.TestCase):
    def test_apply_never_writes_unsupported_supervisor_mirror_configuration(self):
        body = shell_function_body("apply")

        self.assertIn("MIRROR_APPLICATION_UNSUPPORTED", body)
        self.assertNotIn("docker_write_atomic", body)
        self.assertNotIn("supervisor_restart", body)

    def test_startup_self_heal_is_read_only(self):
        body = shell_function_body("self_heal")

        self.assertNotIn("docker_write_atomic", body)
        self.assertNotIn("supervisor_restart", body)

    def test_restore_and_automatic_cycle_cannot_apply_or_restart_mirrors(self):
        for function_name in ("restore_backup", "auto_switch_cycle"):
            body = shell_function_body(function_name)
            self.assertNotIn("docker_write_atomic", body, function_name)
            self.assertNotIn("supervisor_restart", body, function_name)

    def test_legacy_write_requires_a_backup_and_verifies_the_removed_field(self):
        write_body = shell_function_body("docker_write_atomic")
        recovery_body = shell_function_body("recover_direct")

        self.assertIn("无法创建 Supervisor 配置备份", write_body)
        self.assertIn("docker_restore_internal_backup", write_body)
        self.assertIn("LEGACY_RECOVERY_VERIFY_FAILED", recovery_body)
        self.assertIn("has(\"registries_mirror\")", recovery_body)

    def test_legacy_direct_recovery_forgets_old_mirror_snapshot(self):
        body = shell_function_body("recover_direct")
        cleanup_body = shell_function_body("_clear_legacy_state")

        self.assertIn("_clear_legacy_state", body)
        self.assertIn('st["last_known_good"] = None', cleanup_body)
        self.assertIn("has(\"registries_mirror\")", body)
        self.assertIn("docker_restore_internal_backup", body)

    def test_ui_keeps_unsupported_application_controls_disabled(self):
        page = UI.read_text(encoding="utf-8")

        self.assertRegex(page, r'id="btnApply"[^>]*disabled')
        self.assertRegex(page, r'id="btnRestore"[^>]*disabled')
        self.assertIn("const MIRROR_APPLICATION_SUPPORTED=false", page)

    def test_state_field_preserves_dotted_registry_name_as_one_path_segment(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            state_file = Path(temp_dir) / "state.json"
            state_file.write_text(
                json.dumps(
                    {
                        "enabled": {
                            "ghcr.io": True,
                            "docker.io": False,
                            "lscr.io": True,
                        }
                    }
                ),
                encoding="utf-8",
            )
            command = (
                'export SLUG="haos-mirror-switcher" STATE_FILE="$2"; '
                'source "$1"; '
                '_state_field enabled ghcr.io; '
                '_state_field enabled docker.io; '
                '_state_field enabled lscr.io'
            )
            with bash_env_with_python3() as env:
                completed = subprocess.run(
                    ["bash", "-c", command, "actions.sh", ACTIONS.as_posix(), state_file.as_posix()],
                    capture_output=True,
                    text=True,
                    env=env,
                    timeout=10,
                )

        self.assertEqual(0, completed.returncode, completed.stderr)
        self.assertEqual(["true", "false", "true"], completed.stdout.splitlines())

    def test_probe_without_recommendation_is_a_completed_check(self):
        server = load_server_module()
        handler = object.__new__(server.Handler)
        with mock.patch.object(server, "sh", return_value=(True, "all candidates failed", "")):
            with mock.patch.object(
                server,
                "load_state",
                return_value={"recommended": {"ghcr.io": None, "docker.io": None, "lscr.io": None}},
            ):
                response = handler._action(
                    "probe_all",
                    "PROBE_COMPLETED",
                    "检查完成，请确认推荐镜像源后应用",
                    "PROBE_FAILED",
                    "镜像源检查失败，请稍后重试",
                )

        self.assertTrue(response["ok"])
        self.assertEqual("PROBE_COMPLETED_NO_RECOMMENDATION", response["code"])
        self.assertIn("暂未找到可用", response["user_message"])
        self.assertTrue(response["retryable"])

    def test_legacy_recovery_without_mapping_does_not_claim_a_restart(self):
        server = load_server_module()
        handler = object.__new__(server.Handler)
        with mock.patch.object(server, "sh", return_value=(True, "no legacy mapping", "")):
            with mock.patch.object(
                server,
                "load_state",
                return_value={
                    "last_application": {
                        "code": "LEGACY_RECOVERY_NOT_NEEDED",
                        "requires_restart": False,
                    }
                },
            ):
                response = handler._action(
                    "recover_direct",
                    "DIRECT_RESTORED",
                    "已移除镜像映射，Supervisor 正在重启",
                    "DIRECT_RESTORE_FAILED",
                    "恢复直连失败",
                    restart=True,
                )

        self.assertTrue(response["ok"])
        self.assertEqual("LEGACY_RECOVERY_NOT_NEEDED", response["code"])
        self.assertFalse(response["requires_restart"])
        self.assertIn("无需清理", response["user_message"])

    def test_action_log_works_without_bashio_in_child_shell(self):
        command = (
            'export SLUG="haos-mirror-switcher"; '
            'source "$1"; '
            'STATE_FILE="/__missing_haos_mirror_switcher_state__/state.json"; '
            '_log "probe-completed"'
        )
        completed = subprocess.run(
            ["bash", "-c", command, "actions.sh", ACTIONS.as_posix()],
            capture_output=True,
            text=True,
            timeout=10,
        )

        self.assertEqual(0, completed.returncode, completed.stderr)
        self.assertIn("probe-completed", completed.stdout)

    def test_server_forwards_action_output_to_addon_log(self):
        server = load_server_module()
        completed = types.SimpleNamespace(
            communicate=lambda *a, **k: (b"mirror probe completed\n", b""),
            returncode=0,
            kill=lambda: None,
        )

        output = io.StringIO()
        with mock.patch.object(server.subprocess, "Popen", return_value=completed):
            with contextlib.redirect_stdout(output):
                success, stdout, stderr = server.sh("probe_all")

        self.assertTrue(success)
        self.assertEqual("mirror probe completed", stdout)
        self.assertEqual("", stderr)
        self.assertIn("[action:probe_all:stdout] mirror probe completed", output.getvalue())

    def test_server_forwards_failed_action_stderr_to_addon_log(self):
        server = load_server_module()
        completed = types.SimpleNamespace(
            communicate=lambda *a, **k: (b"state updated\n", b"bashio: command not found\n"),
            returncode=1,
            kill=lambda: None,
        )

        output = io.StringIO()
        with mock.patch.object(server.subprocess, "Popen", return_value=completed):
            with contextlib.redirect_stdout(output):
                success, stdout, stderr = server.sh("probe_all")

        self.assertFalse(success)
        self.assertEqual("state updated", stdout)
        self.assertEqual("bashio: command not found", stderr)
        self.assertIn("[action:probe_all:stdout] state updated", output.getvalue())
        self.assertIn("[action:probe_all:stderr] bashio: command not found", output.getvalue())

    def test_server_timeout_kills_child_and_reports(self):
        server = load_server_module()

        class RaisingProc:
            killed = False

            def communicate(self, *args, **kwargs):
                if kwargs.get("timeout") is not None:
                    raise subprocess.TimeoutExpired("bash", kwargs["timeout"])
                return b"partial output\n", b""

            def kill(self):
                self.killed = True

        proc = RaisingProc()
        output = io.StringIO()
        with mock.patch.object(server.subprocess, "Popen", return_value=proc):
            with contextlib.redirect_stdout(output):
                success, stdout, stderr = server.sh("probe_all")

        self.assertTrue(proc.killed)
        self.assertFalse(success)
        self.assertEqual("timeout", stderr)
        self.assertIn("[action:probe_all:stderr] timeout", output.getvalue())

    @unittest.skipIf(os.name == "nt", "the add-on shell runtime is Linux; Windows has no python3 binary")
    def test_probe_summary_includes_empty_and_failed_registries(self):
        fragment = json.dumps(
            {
                "recommended": {
                    "ghcr.io": "ghcr.nju.edu.cn",
                    "docker.io": None,
                    "lscr.io": None,
                },
                "probe_results": {
                    "ghcr.io": {"ghcr.nju.edu.cn": "ok:200|0.12"},
                    "docker.io": {"docker.xuanyuan.me": "fail:000|8.00"},
                },
            },
            ensure_ascii=False,
        )
        completed = subprocess.run(
            [
                "bash",
                "-c",
                'export SLUG="haos-mirror-switcher"; source "$1"; _probe_summary "$2"',
                "actions.sh",
                ACTIONS.as_posix(),
                fragment,
            ],
            capture_output=True,
            text=True,
            timeout=10,
        )

        self.assertEqual(0, completed.returncode, completed.stderr)
        self.assertIn("ghcr.io[ghcr.nju.edu.cn=ok:200|0.12]", completed.stdout)
        self.assertIn("docker.io[docker.xuanyuan.me=fail:000|8.00]", completed.stdout)
        self.assertIn("lscr.io[无候选]", completed.stdout)

    def test_config_version_matches_ghcr_probe_tag(self):
        config = CONFIG.read_text(encoding="utf-8")
        version_match = re.search(r"^version:\s*['\"]([^'\"]+)['\"]\s*$", config, re.MULTILINE)
        self.assertIsNotNone(version_match)
        candidates = json.loads(CANDIDATES.read_text(encoding="utf-8"))
        self.assertEqual(version_match.group(1), candidates["probe"]["ghcr.io"]["tag"])


if __name__ == "__main__":
    unittest.main()
