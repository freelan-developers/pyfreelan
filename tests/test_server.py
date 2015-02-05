"""
Test the web server.
"""

import mock

from unittest import TestCase
from flask import g

from pyfreelan.server import (
    parse_endpoint,
    HTTPServer,
)


class ParsingTests(TestCase):
    def test_parse_endpoint_with_valid_input(self):
        hostname, port = parse_endpoint('this.is.a.host:1234')
        self.assertEqual('this.is.a.host', hostname)
        self.assertEqual(1234, port)

    def test_parse_endpoint_with_valid_ipv6_input(self):
        hostname, port = parse_endpoint('[ffff::0:00:eeee]:1234')
        self.assertEqual('ffff::eeee', hostname)
        self.assertEqual(1234, port)

    def test_parse_endpoint_with_hostname_only_no_default(self):
        hostname, port = parse_endpoint('0.0.0.0')
        self.assertEqual('0.0.0.0', hostname)
        self.assertEqual(0, port)

    def test_parse_endpoint_with_hostname_only_and_default(self):
        hostname, port = parse_endpoint('[::]', default_port=9999)
        self.assertEqual('::', hostname)
        self.assertEqual(9999, port)


class ServerTests(TestCase):
    def test_http_server_parses_configuration(self):
        reactor = mock.MagicMock()
        configuration = {
            'listen_on': '0.0.0.0:1234',
            'secret_key': 'secret',
        }
        callbacks = {
            'sign_certificate_request': None,
        }

        server = HTTPServer(
            reactor=reactor,
            configuration=configuration,
            callbacks=callbacks,
        )

        reactor.listenTCP.assert_called_once_with(
            1234,
            server.site,
            interface='0.0.0.0',
        )
        self.assertEqual(configuration, server.configuration)
        self.assertEqual(callbacks, server.callbacks)

    def test_http_server_registers_into_the_application_context(self):
        reactor = mock.MagicMock()
        configuration = {
            'listen_on': '0.0.0.0:1234',
            'secret_key': 'secret',
        }
        callbacks = {}

        server = HTTPServer(
            reactor=reactor,
            configuration=configuration,
            callbacks=callbacks,
        )

        with server.app.test_request_context('/'):
            self.assertFalse(hasattr(g, 'http_server'))
            server.app.preprocess_request()
            self.assertEqual(getattr(g, 'http_server', None), server)
