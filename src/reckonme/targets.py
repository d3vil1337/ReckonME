"""Strict, offline target parsing shared by configuration and network boundaries."""

from dataclasses import dataclass
import ipaddress
import re
from urllib.parse import quote, urlsplit, urlunsplit


class TargetError(ValueError):
    """A target is malformed or ambiguous."""


@dataclass(frozen=True)
class Target:
    host: str
    kind: str
    scheme: str | None = None
    port: int | None = None
    url: str | None = None

    @property
    def normalized(self) -> str:
        return self.url if self.url is not None else self.host


def normalize_host(value: str) -> tuple[str, str]:
    if not value or any(c.isspace() or ord(c) < 32 for c in value):
        raise TargetError("Host must be nonempty and contain no whitespace or controls.")
    if '%' in value:
        raise TargetError("Encoded hosts and IPv6 zone identifiers are unsupported.")
    try:
        address = ipaddress.ip_address(value)
        return address.compressed, "ip"
    except ValueError:
        pass
    if ':' in value:
        raise TargetError("Invalid IP address; host:port requires an HTTP(S) URL.")
    domain = value[:-1] if value.endswith('.') else value
    try:
        ascii_domain = domain.encode('idna').decode('ascii').lower()
        # Reject lossy IDNA mappings (for example sharp-s -> ss), not identities.
        decoded = ascii_domain.encode('ascii').decode('idna')
        if not domain.isascii() and decoded.lower() != domain.lower():
            raise ValueError("lossy IDNA mapping")
        for label in ascii_domain.split('.'):
            if label.startswith('xn--'):
                if label.encode('ascii').decode('idna').encode('idna').decode('ascii') != label:
                    raise ValueError("invalid punycode")
    except (UnicodeError, ValueError) as exc:
        raise TargetError("Invalid or ambiguous international domain name.") from exc
    labels = ascii_domain.split('.')
    if (len(ascii_domain) > 253 or len(labels) < 2
            or any(not re.fullmatch(r'[a-z0-9](?:[a-z0-9-]{0,61}[a-z0-9])?', x) for x in labels)
            or not re.search(r'[a-z]', labels[-1])):
        raise TargetError("Expected a valid dotted domain name or canonical IP address.")
    # Reject alternate numeric-address spellings accepted by some HTTP clients.
    if all(re.fullmatch(r'(?:[0-9]+|0x[0-9a-f]+)', x) for x in labels):
        raise TargetError("Noncanonical numeric IP addresses are unsupported.")
    return ascii_domain, "domain"


def parse_target(value: str) -> Target:
    if not isinstance(value, str) or not value:
        raise TargetError("Target must be a nonempty string.")
    if any(c.isspace() or ord(c) < 32 or ord(c) == 127 for c in value) or '\\' in value:
        raise TargetError("Target must contain no whitespace, controls or backslashes.")
    if '://' not in value:
        host, kind = normalize_host(value)
        return Target(host, kind)
    try:
        parts = urlsplit(value)
        scheme = parts.scheme.lower()
        if scheme not in ('http', 'https'):
            raise TargetError("Only HTTP and HTTPS URLs are supported.")
        if not parts.netloc or parts.username is not None or parts.password is not None:
            raise TargetError("URL requires a host and must not contain credentials.")
        if parts.netloc.endswith(':'):
            raise TargetError("URL port must be an integer between 1 and 65535.")
        if not re.fullmatch(r'(?:\[[0-9a-fA-F:.]+\]|[^\[\]:]+)(?::[0-9]+)?', parts.netloc):
            raise TargetError("URL authority must contain only a host and optional numeric port.")
        host, kind = normalize_host(parts.hostname or '')
        # urlsplit accepts some noncanonical bracketed host forms; refuse them.
        if parts.netloc.startswith('[') and (kind != 'ip' or ':' not in host):
            raise TargetError("Brackets are reserved for IPv6 URL hosts.")
        if ':' in host and not parts.netloc.startswith('['):
            raise TargetError("IPv6 URL hosts must be enclosed in brackets.")
        port = parts.port
        if port is not None and not 1 <= port <= 65535:
            raise TargetError("URL port must be between 1 and 65535.")
        if re.search(r'%(?![0-9a-fA-F]{2})', parts.path + parts.query + parts.fragment):
            raise TargetError("URL contains an invalid percent escape.")
        effective_port = port or (443 if scheme == 'https' else 80)
        authority = f'[{host}]' if ':' in host else host
        if effective_port != (443 if scheme == 'https' else 80):
            authority += f':{effective_port}'
        path = quote(parts.path or '/', safe="/%:@!$&'()*+,;=-._~")
        query = quote(parts.query, safe="/%?:@!$&'()*+,;=-._~")
        url = urlunsplit((scheme, authority, path, query, ''))
        return Target(host, kind, scheme, effective_port, url)
    except ValueError as exc:
        if isinstance(exc, TargetError):
            raise
        raise TargetError("Malformed URL host, brackets or port.") from exc
