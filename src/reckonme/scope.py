"""Fail-closed scope policy. No DNS resolution or network operations occur here."""

from dataclasses import dataclass

from reckonme.targets import Target, TargetError, parse_target


class ScopeError(ValueError):
    """An otherwise valid target is not authorized by scope."""


@dataclass(frozen=True)
class ScopeRule:
    target: str
    include_subdomains: bool = False
    ports: tuple[int, ...] | None = None

    def __post_init__(self) -> None:
        parsed = parse_target(self.target)
        if type(self.include_subdomains) is not bool:
            raise TargetError("include_subdomains must be a boolean.")
        if self.include_subdomains and (parsed.kind != 'domain' or parsed.url is not None):
            raise TargetError("include_subdomains requires a bare domain rule.")
        if self.ports is not None:
            if (not isinstance(self.ports, tuple) or not self.ports
                    or any(type(p) is not int or not 1 <= p <= 65535 for p in self.ports)):
                raise TargetError("ports must be a nonempty tuple of integers from 1 to 65535.")
            if parsed.url is not None:
                raise TargetError("URL rules already specify a port; ports is not allowed.")
        if parsed.url is not None:
            from urllib.parse import urlsplit
            raw = urlsplit(self.target)
            if raw.path not in ('', '/') or raw.query or raw.fragment or '?' in self.target or '#' in self.target:
                raise TargetError("URL scope rules describe origins only; paths, queries and fragments are unsupported.")
        object.__setattr__(self, 'target', parsed.normalized)

    def matches(self, target: Target) -> bool:
        rule = parse_target(self.target)
        host_matches = target.host == rule.host or (
            self.include_subdomains and target.kind == 'domain'
            and target.host.endswith('.' + rule.host)
        )
        if not host_matches:
            return False
        if rule.url is not None:
            return target.scheme == rule.scheme and target.port == rule.port
        return self.ports is None or target.port in self.ports


@dataclass(frozen=True)
class ScopePolicy:
    include: tuple[ScopeRule, ...]
    exclude: tuple[ScopeRule, ...] = ()

    def __post_init__(self) -> None:
        for rules in (self.include, self.exclude):
            if not isinstance(rules, tuple) or any(not isinstance(r, ScopeRule) for r in rules):
                raise TypeError("Scope rules must be tuples of ScopeRule instances.")

    def require_allowed(self, value: str) -> Target:
        """Validate before I/O; return the normalized target or raise.

        Call for every destination, including redirects. Callers must use the
        returned normalized value and separately constrain DNS/connection behavior.
        """
        target = parse_target(value)
        if any(rule.matches(target) for rule in self.exclude):
            raise ScopeError("Target is explicitly excluded by scope.")
        if not any(rule.matches(target) for rule in self.include):
            raise ScopeError("Target does not match any scope inclusion.")
        return target
