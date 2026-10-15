"""Exercise the installed CLI contract without network activity."""

import os
from pathlib import Path
import subprocess
import sys
import unittest


class ScopeCliTests(unittest.TestCase):
    def run_cli(self, *args):
        root = Path(__file__).resolve().parents[1]
        env = os.environ.copy()
        env['PYTHONPATH'] = str(root / 'src')
        return subprocess.run(
            [sys.executable, '-m', 'reckonme', *args], cwd=root, env=env,
            capture_output=True, text=True, timeout=10, check=False,
        )

    def test_validate_config(self):
        result = self.run_cli('validate-config', '--config', 'examples/scope.toml')
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn('Configuration valid', result.stdout)

    def test_allowed_normalized(self):
        result = self.run_cli('check-scope', '--config', 'examples/scope.toml', 'HTTPS://WWW.EXAMPLE.COM:443/a#fragment')
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(result.stdout.strip(), 'Allowed: https://www.example.com/a')

    def test_denied(self):
        for target in ('https://private.example.com', 'https://example.com.attacker.test'):
            with self.subTest(target=target):
                result = self.run_cli('check-scope', '--config', 'examples/scope.toml', target)
                self.assertEqual(result.returncode, 1)
                self.assertIn('Out of scope', result.stderr)

    def test_invalid_target(self):
        result = self.run_cli('check-scope', '--config', 'examples/scope.toml', 'https://secret:password@example.com')
        self.assertEqual(result.returncode, 2)
        self.assertNotIn('password', result.stderr)
        self.assertNotIn('Traceback', result.stderr)

    def test_missing_config(self):
        result = self.run_cli('validate-config', '--config', 'examples/nonexistent.toml')
        self.assertEqual(result.returncode, 2)
        self.assertNotIn('Traceback', result.stderr)

    def test_required_arguments(self):
        for args in (('check-scope',), ('validate-config',)):
            with self.subTest(args=args):
                self.assertEqual(self.run_cli(*args).returncode, 2)
