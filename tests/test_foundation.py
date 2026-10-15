"""Verify the public CLI contract without invoking any network tools."""

import os
from pathlib import Path
import subprocess
import sys
import unittest


class FoundationTests(unittest.TestCase):
    def run_cli(self, *args: str) -> subprocess.CompletedProcess[str]:
        env = os.environ.copy()
        env["PYTHONPATH"] = str(Path(__file__).resolve().parents[1] / "src")
        return subprocess.run(
            [sys.executable, "-m", "reckonme", *args],
            env=env, capture_output=True, text=True, timeout=10, check=False,
        )

    def test_help(self) -> None:
        result = self.run_cli("--help")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("Recon is not yet implemented", result.stdout)

    def test_version(self) -> None:
        result = self.run_cli("--version")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(result.stdout.strip(), "reckonme 0.1.0")

    def test_unknown_argument_is_rejected(self) -> None:
        result = self.run_cli("--scan")
        self.assertEqual(result.returncode, 2)
        self.assertIn("unrecognized arguments", result.stderr)
