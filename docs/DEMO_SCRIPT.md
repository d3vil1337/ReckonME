# Foundation demo

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
three passing offline tests. Explain the proposed flow in ARCHITECTURE.md and
the distinction between investigation priority and verified severity.
There is no target-scanning demonstration at this milestone.

To demonstrate recovery safeguards, follow BACKUPS.md and inspect archive
verification output. Do not claim a GitHub backup until a push and remote
commit comparison have succeeded.
