"""
Tests command line entry points.
"""

import mock

from unittest import TestCase

from pyfreelan.main import (
    client_main,
    server_main,
)


class MainTests(TestCase):
    @mock.patch('twisted.internet.reactor.run')
    def test_pyfreelan_server_launches_fine(self, reactor_mock):
        server_main()
        reactor_mock.assert_called_with()

    @mock.patch('twisted.internet.reactor.run')
    def test_pyfreelan_client_launches_fine(self, reactor_mock):
        client_main()
        reactor_mock.assert_called_with()
