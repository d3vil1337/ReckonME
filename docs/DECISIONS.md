# Decisions

- 2026-10-15: use standard-library TOML, strict unknown-key rejection and immutable
  scope objects. Require explicit subdomains; exclude always wins. URL rules are
  origins, not path prefixes. See SCOPE.md for exact normalization and limitations.
- 2026-10-15: owner approved the configuration/scope milestone for commit, push
  and external archive after final verification. Preserve foundation history and
  stop before the next implementation milestone.

- 2026-10-15: Python 3.11+, src-layout package, argparse and unittest. This keeps
  the foundation small and runtime dependencies at zero.
- 2026-10-15: setuptools is a build dependency only; editable installation and
  direct source execution are documented separately.
- 2026-10-15: SQLite will preserve scan history and evidence with transactional
  integrity; no database is created in the foundation.
- 2026-10-15: scope enforcement precedes network execution. Filtering collected
  output is insufficient because unauthorized requests may already have occurred.
- 2026-10-15: a dated source ZIP plus a Git bundle provides independent recovery
  of committed source and history. Only tracked committed content is archived;
  scan data and credentials require separate storage and must never enter Git.
- 2026-10-15: no remote is presumed. The owner creates a private GitHub repository
  and authenticates before a push can be verified.
