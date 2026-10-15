# Learning guide

The CLI translates terminal arguments into application behavior. `argparse`
supplies help, version and rejection of unsupported flags. It performs
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

Configuration is now a strict TOML document: a misspelled option fails instead of
silently disabling a restriction. Frozen data classes keep the validated policy
from changing accidentally. See SCOPE.md and examples/scope.toml.

Validation asks whether a target is well formed; authorization asks whether it is
allowed. `require_allowed` does both, returning a normalized target only on success.
Exclusions always win. Subdomain checks require a dot boundary, so an attacker's
`example.com.attacker.test` cannot borrow permission from `example.com`.

An origin is scheme + host + port. An HTTPS origin rule grants its paths, but
does not grant HTTP or another port. A host rule is broader unless ports are
specified. DNS names and the IPs they resolve to are different identities:
connection-time DNS protections still need to be implemented with future adapters.

Tests exercise malformed files, deceptive hosts, normalization, policy boundaries,
and CLI exit codes without sending network requests. A redirect simulation checks
the new URL through policy; no HTTP client or redirect interceptor exists yet.
