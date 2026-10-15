"""Offline adversarial boundary and configuration checks."""

import copy
from pathlib import Path
import socket
import tempfile
import unittest
from unittest.mock import patch

from reckonme.config import ConfigError, load_config, parse_config
from reckonme.scope import ScopeError, ScopePolicy, ScopeRule
from reckonme.targets import TargetError, parse_target


class TargetTests(unittest.TestCase):
    def test_domains(self):
        for raw, expected in [('EXAMPLE.com.', 'example.com'), ('a-b.example.com', 'a-b.example.com'),
                              ('bücher.example', 'xn--bcher-kva.example'), ('xn--bcher-kva.example', 'xn--bcher-kva.example')]:
            with self.subTest(raw=raw):
                self.assertEqual(parse_target(raw).host, expected)

    def test_ips(self):
        for raw, expected in [('192.0.2.1', '192.0.2.1'), ('2001:0db8::1', '2001:db8::1'),
                              ('::1', '::1')]:
            with self.subTest(raw=raw):
                self.assertEqual(parse_target(raw).host, expected)
        self.assertEqual(parse_target('::ffff:192.0.2.1').host, parse_target('::ffff:c000:201').host)

    def test_url_normalization(self):
        cases = [('HTTPS://EXAMPLE.com.:443', 'https://example.com/'),
                 ('http://example.com:80/a?q=x#frag', 'http://example.com/a?q=x'),
                 ('https://[2001:0db8::1]:8443/a', 'https://[2001:db8::1]:8443/a'),
                 ('https://bücher.example/é?q=é', 'https://xn--bcher-kva.example/%C3%A9?q=%C3%A9'),
                 ('https://example.com/a%2Fb?x=1&x=2', 'https://example.com/a%2Fb?x=1&x=2')]
        for raw, expected in cases:
            with self.subTest(raw=raw):
                self.assertEqual(parse_target(raw).normalized, expected)
                self.assertEqual(parse_target(expected).normalized, expected)

    def test_invalid_targets(self):
        values = ['', None, 4, ' example.com', 'example.com ', 'example..com', '-a.example',
                  'a-.example', 'a_b.example', 'localhost', '*.example.com', 'example.com..',
                  '999.2.3.4', '127.1', '0177.0.0.1', '0x7f.0.0.1', '2130706433',
                  '192.0.2.0/24', '[::1]', 'fe80::1%eth0', 'example.com:80', 'faß.example',
                  'xn--.example', 'a'*64 + '.example', 'a.'*127 + 'example',
                  'ftp://example.com', '//example.com', 'https:///path',
                  'https://user:secret@example.com', 'https://example.com@attacker.test',
                  'https://example.com:', 'https://example.com:0', 'https://example.com:65536',
                  'https://example.com:no', 'https://[::1', 'https://::1/',
                  'https://%65xample.com', 'https://example.com/a%xx',
                  'https://[::1]attacker.test', 'https://[::1]:443attacker',
                  'https://example.com/\\evil', 'https://example.com/\nfoo',
                  'https://example.com/\tfoo', 'https://example.com/\x7ffoo']
        for value in values:
            with self.subTest(value=value), self.assertRaises(TargetError):
                parse_target(value)

    def test_port_limits(self):
        for port in (1, 65535):
            self.assertEqual(parse_target(f'https://example.com:{port}').port, port)


class PolicyTests(unittest.TestCase):
    def test_deny_default(self):
        with self.assertRaises(ScopeError):
            ScopePolicy(()).require_allowed('example.com')

    def test_exact_domain(self):
        policy = ScopePolicy((ScopeRule('example.com'),))
        for value in ('example.com', 'https://EXAMPLE.com:8443/a'):
            self.assertEqual(policy.require_allowed(value).host, 'example.com')
        for value in ('a.example.com', 'example.com.attacker.test', 'evil-example.com'):
            with self.subTest(value=value), self.assertRaises(ScopeError):
                policy.require_allowed(value)

    def test_subdomain_boundary(self):
        policy = ScopePolicy((ScopeRule('example.com', True),))
        for value in ('example.com', 'a.example.com', 'https://a.b.example.com/'):
            policy.require_allowed(value)
        for value in ('example.com.attacker.test', 'badexample.com', 'examplecom.test'):
            with self.subTest(value=value), self.assertRaises(ScopeError):
                policy.require_allowed(value)

    def test_exclusions_override(self):
        policy = ScopePolicy((ScopeRule('example.com', True), ScopeRule('private.example.com')),
                             (ScopeRule('private.example.com', True),))
        policy.require_allowed('public.example.com')
        for value in ('private.example.com', 'https://a.private.example.com/'):
            with self.subTest(value=value), self.assertRaisesRegex(ScopeError, 'excluded'):
                policy.require_allowed(value)

    def test_origin_scheme_port_and_paths(self):
        policy = ScopePolicy((ScopeRule('https://example.com'),))
        for value in ('https://example.com/a?x=1', 'https://example.com:443/../b'):
            policy.require_allowed(value)
        for value in ('example.com', 'http://example.com', 'https://example.com:8443', 'https://a.example.com'):
            with self.subTest(value=value), self.assertRaises(ScopeError):
                policy.require_allowed(value)

    def test_origin_exclusion(self):
        policy = ScopePolicy((ScopeRule('example.com'),), (ScopeRule('https://example.com:8443'),))
        policy.require_allowed('https://example.com')
        with self.assertRaises(ScopeError):
            policy.require_allowed('https://example.com:8443/private')

    def test_port_restricted_host(self):
        policy = ScopePolicy((ScopeRule('192.0.2.1', ports=(443,)),))
        policy.require_allowed('https://192.0.2.1/a')
        for value in ('192.0.2.1', 'http://192.0.2.1', 'https://192.0.2.2'):
            with self.subTest(value=value), self.assertRaises(ScopeError):
                policy.require_allowed(value)

    def test_ipv6_and_idn(self):
        ScopePolicy((ScopeRule('2001:db8::1'),)).require_allowed('https://[2001:0db8::1]')
        ScopePolicy((ScopeRule('bücher.example', True),)).require_allowed('https://a.xn--bcher-kva.example')
        with self.assertRaises(ScopeError):
            ScopePolicy((ScopeRule('192.0.2.1'),)).require_allowed('::ffff:192.0.2.1')

    def test_invalid_rules(self):
        cases = [('192.0.2.1', True, None), ('https://example.com', True, None),
                 ('example.com', 'yes', None), ('example.com', False, (True,)),
                 ('example.com', False, (0,)), ('example.com', False, (65536,)),
                 ('example.com', False, ()), ('example.com', False, [443]),
                 ('https://example.com', False, (443,))]
        for args in cases:
            with self.subTest(args=args), self.assertRaises(TargetError):
                ScopeRule(*args)
        for suffix in ('/path', '?x=1', '#frag', '?', '#'):
            with self.subTest(suffix=suffix), self.assertRaises(TargetError):
                ScopeRule('https://example.com' + suffix)

    def test_malformed_never_allowed(self):
        with self.assertRaises(TargetError):
            ScopePolicy((ScopeRule('example.com'),)).require_allowed('https://example.com:bad')

    def test_each_redirect_must_be_checked(self):
        policy = ScopePolicy((ScopeRule('example.com'),))
        policy.require_allowed('https://example.com/start')
        with self.assertRaises(ScopeError):
            policy.require_allowed('https://attacker.test/redirected')

    def test_policy_does_not_resolve_dns(self):
        with patch.object(socket, 'getaddrinfo', side_effect=AssertionError('DNS forbidden')):
            ScopePolicy((ScopeRule('example.com'),)).require_allowed('https://example.com')

    def test_policy_requires_immutable_rule_collections(self):
        with self.assertRaises(TypeError):
            ScopePolicy([ScopeRule('example.com')])


class ConfigurationTests(unittest.TestCase):
    def valid(self):
        return {'version': 1, 'scope': {'include': [{'target': 'example.com', 'include_subdomains': True}]}}

    def test_valid_and_exclusions(self):
        doc = self.valid()
        doc['scope']['exclude'] = [{'target': 'private.example.com'}]
        config = parse_config(doc)
        config.scope.require_allowed('a.example.com')
        with self.assertRaises(ScopeError):
            config.scope.require_allowed('private.example.com')

    def test_configuration_detached_from_input(self):
        doc = self.valid()
        config = parse_config(doc)
        doc['scope']['include'].clear()
        config.scope.require_allowed('example.com')

    def test_invalid_documents(self):
        docs = [None, [], {}, {'version': 1}, {'version': 1, 'scope': []}]
        for version in (True, 2, '1', 1.0):
            doc = self.valid(); doc['version'] = version; docs.append(doc)
        doc = self.valid(); doc['unexpected'] = 1; docs.append(doc)
        for scope in ({}, {'include': []}, {'include': 'example.com'},
                      {'include': [{}]}, {'include': [3]}, {'include': [{'target': None}]},
                      {'include': [{'target': 'example.com', 'typo': True}]},
                      {'include': [{'target': 'example.com', 'include_subdomains': 'yes'}]},
                      {'include': [{'target': 'example.com', 'ports': [True]}]},
                      {'include': [{'target': 'example.com', 'ports': '443'}]},
                      {'include': [{'target': 'https://example.com/path'}]},
                      {'include': [{'target': 'example.com'}], 'exclude': {}},
                      {'include': [{'target': 'example.com'}], 'typo': []}):
            docs.append({'version': 1, 'scope': scope})
        for doc in docs:
            with self.subTest(doc=doc), self.assertRaises(ConfigError):
                parse_config(copy.deepcopy(doc))

    def test_load_example(self):
        config = load_config(Path(__file__).resolve().parents[1] / 'examples/scope.toml')
        config.scope.require_allowed('https://www.example.com')
        config.scope.require_allowed('https://192.0.2.1')

    def test_file_failures_are_clear_and_redacted(self):
        with tempfile.TemporaryDirectory() as temp:
            path = Path(temp) / 'config.toml'
            for content in (b'version = [SECRET', b'\xff', b'version=1\nversion=1'):
                path.write_bytes(content)
                with self.assertRaises(ConfigError) as caught:
                    load_config(path)
                self.assertNotIn('SECRET', str(caught.exception))
            with self.assertRaises(ConfigError):
                load_config(Path(temp) / 'absent.toml')
            with self.assertRaises(ConfigError):
                load_config(temp)

    def test_valid_port_rule(self):
        doc = self.valid()
        doc['scope']['include'][0]['ports'] = [443, 8443]
        parse_config(doc).scope.require_allowed('https://example.com:8443')
