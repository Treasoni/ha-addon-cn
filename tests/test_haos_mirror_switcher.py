import contextlib
import importlib.util
import io
import json
import os
import re
import subprocess
import sys
import types
import unittest
from pathlib import Path
from unittest import mock


ROOT = Path(__file__).resolve().parents[1]
ACTIONS = ROOT / "haos-mirror-switcher" / "lib" / "actions.sh"
SERVER = ROOT / "haos-mirror-switcher" / "server.py"
CONFIG = ROOT / "haos-mirror-switcher" / "config.yaml"
CANDIDATES = ROOT / "haos-mirror-switcher" / "lib" / "candidates.json"


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
