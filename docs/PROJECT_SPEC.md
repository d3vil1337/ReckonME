# Product specification

## Purpose and invariants

Discover assets, correlate evidence, prioritize investigations, explain findings,
track changes and support structured investigations. Investigation priority and
confirmed vulnerability severity are separate concepts. Heuristics and AI text
must remain explicitly unverified hypotheses. Core functionality requires no AI
credentials. Only authorized, configured targets may receive network operations.

## Planned milestones and acceptance criteria

0. Foundation (current): durable documents, minimal packaged CLI, ignore rules,
   passing offline smoke tests, local Git checkpoint and verified dated archive.
1. Configuration and scope: validated explicit allow/deny policy, clear CLI errors,
   logging with secret redaction and offline tests for domain boundaries, ports,
   IP addresses, IDNs, malformed URLs, redirects and deny precedence. Document
   supported scope semantics before allowing network operations.
2. Recon vertical slice: dependency checks for Subfinder, ProjectDiscovery httpx
   and Katana; argument-list subprocesses, timeouts, cancellation and clear
   missing-tool failures. Start with a scope-controlled adapter workflow, SQLite
   scan/evidence persistence, deduplication and JSON/TXT export. Verify with fake
   executables offline; any live test requires owner-authorized scope.
3. Deterministic analysis: endpoint classification and explainable investigation
   scoring with evidence, rule versions, confidence and no vulnerability claims.
4. JavaScript analysis: route/API indicators with source URL, extraction location
   and evidence attribution; bounded parsing and scope-controlled fetching.
5. History: resumable stages, idempotent writes and scan comparisons that never
   label missing assets as removed when discovery was incomplete.
6. Reports: stable JSON schema, TXT and, if feasible, escaped standalone HTML;
   explicit completeness and provenance on every report.
7. Optional AI: provider abstraction, opt-in data handling, unavailable-provider
   fallback and hypotheses linked to original evidence. Deterministic core works
   unchanged without credentials.
8. Release readiness: installation and dependency checks, automated regression
   tests, migration policy, docs and reproducible demo. Web UI is a later phase
   requiring a reliable core and separate owner approval.

## Cross-cutting acceptance

Maintain typed boundaries where useful, modular components, actionable errors,
bounded resource use and minimal dependencies. Persist scan status and evidence
provenance. No implicit shell execution, secret commits or silent partial scans.
Each milestone includes tests, diff review, accurate documentation, Git checkpoint
and verified independent archive. Owner approval gates every next major milestone.
