# Verified project state

Date: 2026-10-15 (Asia/Calcutta). Milestone: configuration and offline scope enforcement, approved, committed, pushed and archived.

## Implemented

Python src-layout package, help/version CLI, strict TOML configuration loading,
offline domain/IP/HTTP(S) target validation, immutable scope rules, deny-by-default
authorization with exclusions, and validate-config/check-scope CLI commands.
See SCOPE.md for complete semantics. Added adversarial policy/configuration tests
and CLI integration tests. No network operations, recon adapters, SQLite database,
scoring, AI, JavaScript intelligence or UI exist yet.

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
- GitHub CLI, Subfinder, httpx and Katana were not found on PATH during foundation
  inspection. Remote origin is now configured as https://github.com/d3vil1337/ReckonME.git
  (owner-designated private repository). Successful push/hash verification is recorded below.

## Current milestone verification

- Full command: `.\.venv\Scripts\python.exe -m unittest discover -s tests -v`.
- Result: 33 tests passed in 1.978 seconds on Python 3.12.14, including the original
  3 foundation tests. Subtests cover additional invalid inputs and boundaries.
- Full suite ran outside the sandbox because temporary-file configuration tests
  encountered sandbox permission errors; no tests were skipped.
- Earlier run found an IPv4-mapped IPv6 representation expectation difference;
  the test now verifies equivalent addresses normalize identically across runtime
  representations. Authority review added rejection of bracketed IPv6 trailing text.
- No live targets contacted. No dependencies added; Python 3.11+ standard library.
- Six manual CLI checks from DEMO_SCRIPT.md returned the expected exit codes:
  0, 0, 1, 1, 0, 2. These cover valid configuration, allowed domain, exclusion,
  deceptive suffix, explicit origin/port, and malformed URL port.
- Diff review found no unrelated deletions. `git diff --check` passed; all 16
  modified/new text files passed trailing-whitespace and credential-pattern checks.
  Foundation commits and archives are preserved.
- Verified implementation commit: `e08c97dc88310420d2a4d674f8bec108e30e84ad`.
  Message: Add strict configuration loading and reusable offline scope enforcement.
- `git push -u origin main` succeeded. `git rev-parse HEAD` and
  `git ls-remote origin refs/heads/main` both returned the implementation hash above.
- The documented backup script created and verified this milestone archive:
  C:\Users\WhiteDevil\.codex\visualizations\2026\10\15\01a13f74-9fe3-7b93-ac6a-ebc454b68b16\ReckonME_Backups\20261015-181614-134-e08c97dc8831
- Independently recomputed SHA-256 values match SHA256.txt:
  - source.zip: `6598DF3443DC77426CBA4391A598E9A354A907F352AD9452FF1F185E0C5A45C7`
  - history.bundle: `4DDA4D7702C006B250D607964EC785534836CB7B6CFCF927EE0F63DE201D0E43`
- `git bundle verify` passed with complete history; the archive MANIFEST records
  the implementation commit. ZIP entry verification also passed in the script.
  The bundle includes all refs, including local Codex checkpoint refs; source.zip
  contains HEAD files. Local Git settings, ignored data and reflogs are not backed up.
- This verification record is saved in a separate documentation-only follow-up
  commit. Its final commit/push/archive identity is recorded by Git and the later
  archive MANIFEST, avoiding a self-referential hash or future-success assertion.

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

Stop after preserving this verification record and its final remote/archive
checkpoint. Next implementation milestone requires new approval: design
scope-constrained tool adapters, dependency checks and fake-tool integration tests
before live recon. Do not implement the recon engine yet.

Current limitations: DNS resolution/connection policy and redirect interception
are not implemented; require_allowed must be called by every future adapter.
CIDRs, single-label hosts and URL path-based rules are intentionally unsupported.
Python built-in IDNA is used with lossy mappings rejected. Logging/redaction
infrastructure from the wider specification is deferred until an execution layer
exists; current error messages avoid echoing raw targets/configuration content.
