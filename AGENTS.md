# ReckonME working instructions

Read README.md and docs/PROJECT_STATE.md first, then PROJECT_SPEC.md,
ARCHITECTURE.md and DECISIONS.md. Preserve existing work and Git history.

Python, CLI first, SQLite persistence, deterministic analysis, optional
provider-independent AI. Do not implement a UI before the core is reliable.
Never describe priority scores or hypotheses as confirmed vulnerabilities.
Enforce configured scope before every future network operation, including
redirects, crawling and child-tool operations. Do not run recon against real
targets without explicit authorization and scope.

Work in small milestones. Explain the objective, inspect code, implement,
test, review the diff and secret exposure, update durable documentation,
commit and verify an external dated archive. Stop for owner approval before
the next major milestone. Never invent test results or backup status.

Never commit credentials, .env, scan data, reports or virtual environments.
No destructive Git commands or deletion of user data without explicit approval.
Before risky changes create and verify a checkpoint. Keep dependencies minimal.
Use `python -m unittest discover -s tests -v`; document unavailable checks.

Current milestone is configuration and offline scope enforcement. No recon engine,
AI or web UI. The owner approved committing, pushing and archiving this milestone.
Do not start the next implementation milestone without approval. Do not claim an
archive contains uncommitted work: the backup script archives committed data only.
