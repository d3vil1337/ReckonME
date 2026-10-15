# Architecture plan

Only the package entry point exists today. The following is a design plan.

CLI -> validated configuration -> scope policy -> orchestration -> tool adapters
-> normalized observations -> SQLite -> deterministic analysis -> reports.
Optional AI consumes selected evidence behind a provider interface; it is never
on the required execution path and cannot turn a hypothesis into a verified fact.

Planned modules: config, scope, orchestration, adapters, storage, analysis,
javascript, history, reports and optional ai. Introduce modules when implemented,
rather than filling the repository with empty abstractions.

Adapters use explicit executable paths and argv lists with shell disabled,
bounded output/time, exit-status checks and cancellation. Tool-generated network
requests must be constrained by validated scope; output filtering alone cannot
enforce scope. Block integrations whose behavior cannot meet that requirement.

## Proposed database model

- scans: ID, configuration fingerprint, timestamps, overall status and version.
- stages: scan ID, adapter version, status, completion marker and errors.
- assets/endpoints: normalized identifiers, unique within documented identity rules.
- observations: scan/stage ID, asset, evidence type, source, time and raw evidence reference.
- assessments: rule/version, priority, confidence and linked observation IDs.
- schema_migrations: explicit schema version and applied time.

Use foreign keys, transactions and unique constraints for integrity. Preserve
observations across scans rather than overwriting historical evidence. Resumption
uses stage completion and idempotent writes. Diffs distinguish added, observed,
absent and unknown due to incomplete coverage. SQLite and migrations are not yet
implemented. Sensitive raw output stays out of source control.

Tests progress from offline policy/unit tests to fake tool integration and
temporary SQLite tests. Live recon is a separately authorized validation step.
