# ReckonME

Evidence-driven attack-surface intelligence for security researchers and bug
bounty hunters. **Foundation only:** the CLI currently provides help and version;
discovery, network access, analysis and persistence are not implemented.

## Setup

Install Python 3.11+ and Git. From the project root in PowerShell:

```powershell
py -3 -m venv .venv
.\.venv\Scripts\python.exe -m pip install -e .
.\.venv\Scripts\reckonme.exe --help
.\.venv\Scripts\reckonme.exe --version
.\.venv\Scripts\python.exe -m unittest discover -s tests -v
```

Editable installation uses setuptools and may require a download. The source
workflow needs no third-party packages:

```powershell
$env:PYTHONPATH = "$PWD\src"
python -m reckonme --help
python -m unittest discover -s tests -v
```

Use an actual Python executable if `python` resolves to a Windows Store alias.
Subfinder, ProjectDiscovery httpx and Katana will be optional external tools for
later milestones; they are not needed or invoked now. Dependency validation must
distinguish ProjectDiscovery httpx from similarly named Python tools.

## Project memory and backups

See [project state](docs/PROJECT_STATE.md), [specification](docs/PROJECT_SPEC.md),
[architecture](docs/ARCHITECTURE.md), [learning guide](docs/LEARNING_GUIDE.md),
[demo](docs/DEMO_SCRIPT.md) and [backup instructions](docs/BACKUPS.md).
Local commits are checkpoints, not remote backups. Scan data belongs in ignored
directories and needs a separate, private retention policy when implemented.
