# Offline configuration and scope demo

Run from the project root with Python 3.11+ (`python` must be a real interpreter):

```powershell
$env:PYTHONPATH = "$PWD\src"
python -m reckonme --help
python -m reckonme --version
python -m unittest discover -s tests -v
git log -1 --oneline
git status --short
```

Expect help to state recon is not implemented, version `reckonme 0.1.0`, and
33 passing offline tests. Explain the proposed flow in ARCHITECTURE.md and
the distinction between investigation priority and verified severity.
There is no target-scanning demonstration at this milestone.

To demonstrate recovery safeguards, follow BACKUPS.md and inspect archive
verification output. Do not claim a GitHub backup until a push and remote
commit comparison have succeeded.

## Scope checks (PowerShell)

```powershell
.\.venv\Scripts\python.exe -m reckonme validate-config --config examples/scope.toml
.\.venv\Scripts\python.exe -m reckonme check-scope --config examples/scope.toml https://www.example.com
.\.venv\Scripts\python.exe -m reckonme check-scope --config examples/scope.toml https://private.example.com
.\.venv\Scripts\python.exe -m reckonme check-scope --config examples/scope.toml https://example.com.attacker.test
.\.venv\Scripts\python.exe -m reckonme check-scope --config examples/scope.toml https://api.example.test:8443/path
.\.venv\Scripts\python.exe -m reckonme check-scope --config examples/scope.toml https://example.com:bad
```

Expected exit codes in order: 0, 0, 1, 1, 0, 2. In PowerShell inspect
`$LASTEXITCODE` immediately after each invocation. All checks are offline.
