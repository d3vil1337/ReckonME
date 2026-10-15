"""Central, strict TOML configuration loading; no implicit environment overrides."""

from dataclasses import dataclass
from pathlib import Path
import tomllib

from reckonme.scope import ScopePolicy, ScopeRule
from reckonme.targets import TargetError


class ConfigError(ValueError):
    """Configuration cannot be read or validated."""


@dataclass(frozen=True)
class Config:
    scope: ScopePolicy
    version: int = 1


def _rules(value: object, field: str) -> tuple[ScopeRule, ...]:
    if not isinstance(value, list):
        raise ConfigError(f'{field} must be an array of rule tables.')
    rules = []
    for index, entry in enumerate(value):
        label = f'{field}[{index}]'
        if not isinstance(entry, dict) or set(entry) - {'target', 'include_subdomains', 'ports'}:
            raise ConfigError(f'{label} must be a rule table with only target, include_subdomains and ports.')
        if 'target' not in entry:
            raise ConfigError(f'{label}.target is required.')
        ports = entry.get('ports')
        if 'ports' in entry and not isinstance(ports, list):
            raise ConfigError(f'{label}.ports must be an array of integers.')
        try:
            rules.append(ScopeRule(entry['target'], entry.get('include_subdomains', False),
                                   tuple(ports) if ports is not None else None))
        except (TargetError, TypeError) as exc:
            raise ConfigError(f'{label}: {exc}') from exc
    return tuple(rules)


def parse_config(document: object) -> Config:
    if not isinstance(document, dict) or set(document) != {'version', 'scope'}:
        raise ConfigError('Configuration requires exactly version and scope fields.')
    if type(document['version']) is not int or document['version'] != 1:
        raise ConfigError('version must be integer 1.')
    scope = document['scope']
    if not isinstance(scope, dict) or 'include' not in scope or set(scope) - {'include', 'exclude'}:
        raise ConfigError('scope requires include and permits only include and exclude.')
    include = _rules(scope['include'], 'scope.include')
    exclude = _rules(scope.get('exclude', []), 'scope.exclude')
    if not include:
        raise ConfigError('scope.include must contain at least one rule.')
    return Config(ScopePolicy(include, exclude))


def load_config(path: str | Path) -> Config:
    try:
        with Path(path).open('rb') as stream:
            document = tomllib.load(stream)
    except (OSError, ValueError) as exc:
        # Avoid echoing TOML lines that might contain private material.
        raise ConfigError('Cannot read configuration as valid UTF-8 TOML; check path, permissions and syntax.') from exc
    return parse_config(document)
