# Configuration and scope contract

Use an explicit TOML file; there is no implicit search, environment expansion,
secret loading, include-file support or configuration merging. Python's standard
library tomllib parses it. Unknown fields, missing fields and wrong types fail.

```toml
version = 1

[[scope.include]]
target = "example.com"
include_subdomains = true
ports = [443, 8443]

[[scope.exclude]]
target = "private.example.com"
include_subdomains = true
```

Exactly `version` and `scope` are required at the top level. Version must be
integer 1. Scope requires a nonempty `include` array and permits an optional
`exclude` array. Each rule requires `target`, with optional boolean
`include_subdomains` (default false) and nonempty integer `ports` array (1–65535).
Rules and loaded configuration are immutable and detached from input dictionaries.

## Matching

- Deny unless an inclusion matches. Any matching exclusion overrides all inclusions.
- Bare domains match the exact host, on all schemes/ports unless restricted.
  `include_subdomains = true` also matches descendant DNS labels, including deep
  descendants; `example.com.attacker.test` and `badexample.com` do not match.
- Bare IPs match the same normalized address; IPv4-mapped IPv6 stays a separate
  identity from IPv4. There is no CIDR support or DNS lookup.
- URL rules match an exact scheme, host and effective port (an origin), for all
  request paths and queries. Only empty/root paths are accepted in rules; query
  strings and fragments are rejected. Subdomain and separate ports options are
  forbidden on URL rules. HTTP defaults to 80; HTTPS defaults to 443.
- A ports-restricted bare-host rule cannot authorize a bare-host target: that
  target lacks a port. Submit the actual URL before making a request.
- An origin-only exclusion denies that origin, not a bare-host discovery target.
  Future adapters must check the actual destination URL, even after a host check.

## Target validation and normalization

Targets are dotted DNS names, IP literals, or absolute HTTP(S) URLs. Domains are
lowercased, a single trailing root dot removed, and IDNs converted with Python's
IDNA codec. Lossy mappings such as sharp-s to ss are rejected. This is Python's
built-in IDNA behavior, not full IDNA2008/UTS46 browser compatibility. Unicode and
punycode equivalents share a host identity; visually confusable names do not.
Single-label names, wildcards, CIDRs and noncanonical numeric IPv4 forms are rejected.

IP addresses use ipaddress normalization; IPv6 URL hosts require brackets. URL
credentials, whitespace, controls, backslashes, encoded hosts, IPv6 zone identifiers,
invalid brackets, empty/invalid ports and malformed percent escapes are rejected.
Default ports are omitted from normalized URLs; an empty path becomes `/`;
fragments are removed; Unicode path/query characters are UTF-8 percent encoded.
Existing valid escapes, path case, dot segments and query ordering are preserved.
Scope does not depend on paths, so path normalization cannot broaden an origin rule.

## Reusable boundary

```python
from reckonme.config import load_config

config = load_config("examples/scope.toml")
destination = config.scope.require_allowed("https://www.example.com/path")
# Future network code must use destination.normalized only after this succeeds.
```

`TargetError` rejects malformed inputs, `ConfigError` rejects configuration, and
`ScopeError` rejects unauthorized targets. Error messages avoid echoing raw targets
or TOML content, which might contain credentials. There is no logging subsystem
yet; callers must avoid logging raw input. This milestone adds no network code.

Every future network module must recheck redirects, crawl links, JavaScript
fetches, and child-tool destinations before I/O. This API is a hostname/origin
authorization decision, not a DNS rebinding defense or a sandbox for external
tools. Adapters must separately enforce resolved-IP/connection policy, pin checked
destinations as needed, and disable or intercept automatic redirects. Output
filtering after a tool runs cannot enforce these requirements.
