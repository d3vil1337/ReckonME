# Learning guide

The CLI translates terminal arguments into application behavior. `argparse`
currently supplies help, version and rejection of unsupported flags. It performs
no recon. `src/` separates installable code from tests and project documents.

A test launches a fresh Python process and checks the actual CLI exit status and
output. This catches broken imports as well as argument handling. Passing these
tests establishes a working entry point, not a working security scanner.

Future adapters will translate external tools into consistent observations.
Scope policy answers whether an operation is allowed before the tool runs.
SQLite will connect each observation to its scan and source so a researcher can
explain why an endpoint was prioritized and compare evidence over time.

Priority means “investigate this first.” Severity describes the impact of a
verified vulnerability. A suspicious endpoint alone does not establish impact.

A Git commit is a recoverable local snapshot. A remote push protects against
local loss. An archive outside the project protects against accidental project
deletion, but an archive on the same machine does not protect against device loss.
Keep a verified copy on separate storage for that risk.
