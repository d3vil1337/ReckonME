# Verified project state

Date: 2026-10-15 (Asia/Calcutta). Milestone: foundation only.

## Implemented

Minimal Python src-layout package, help/version CLI, three offline subprocess
smoke tests, permanent project documentation, ignore rules and dated external
source ZIP/Git bundle backup script. No network operations, recon adapters,
SQLite database, scoring, AI or UI exist yet.

## Environment and validation

- Project: F:\ReckonMe_OTG; initially empty, no existing Git repository/history.
- Git 2.51.0.windows.1; local author identity already configured.
- System Python is an unusable Windows Store alias; `py` reports no installed Python.
- Bundled interpreter used: C:\Users\WhiteDevil\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe
- Bundled Python version: 3.12.14.
- `python -m unittest discover -s tests -v`: 3 tests passed using bundled Python,
  and again using the project virtual environment before installation.
- Virtual environment setup and editable installation succeeded outside the sandbox
  after sandbox temporary-file permissions blocked the first attempt.
- `.venv\Scripts\python.exe -m pip install --no-build-isolation --no-deps -e .`:
  built and installed reckonme 0.1.0 successfully.
- `.venv\Scripts\reckonme.exe --version`: `reckonme 0.1.0`.
- Ignore checks confirmed exclusion of .env, virtual environments, scan data,
  reports and private-key filename patterns. `git diff --check` passed.
- GitHub CLI, Subfinder, httpx and Katana were not found on PATH. No remote is
  configured; GitHub authentication and remote backup are unverified.

## Checkpoints and archive procedure

Initial Git branch: main. Commit history and external archive verification output
are the authoritative checkpoint records. Run scripts/backup.ps1 after committing;
the archive MANIFEST records the exact commit without a self-referential hash here.
Initial archive destination:
C:\Users\WhiteDevil\.codex\visualizations\2026\10\15\01a13f74-9fe3-7b93-ac6a-ebc454b68b16\ReckonME_Backups

This is outside the project on a different drive path, but hardware independence
and off-device durability are not established. See BACKUPS.md for owner-managed
storage and private GitHub setup. The script verifies the Git bundle and ZIP
entry list and writes hashes. Initial checkpoint `4a23a3d` was archived with a
complete, verified Git bundle and matching ZIP entry list. Extracting source.zip
into a separate restore-check directory and running its tests passed all 3 tests.
Later documentation checkpoints use the same archive procedure; consult the
latest archive MANIFEST for its exact commit.

## Known limitations and exact next task

Foundation smoke tests do not establish scanner correctness. Normal installation
with a separately installed Python and isolated build dependencies has not been
tested on this machine. No license has been selected by the owner.

Stop for owner review. After approval, implement milestone 1: configuration schema,
CLI validation, explicit scope semantics and offline scope-policy tests before
adding any network-capable integrations. Keep provider AI and UI out of that scope.
