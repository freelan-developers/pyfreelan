"""
Tests command line entry points.
"""

import mock

from unittest import TestCase

from tornado.ioloop import IOLoop
from pyfreelan.main import (
    client_main,
    server_main,
)

class MainTests(TestCase):
    @mock.patch('tornado.ioloop.IOLoop.instance')
    def test_pyfreelan_server_launches_an_ioloop(self, instance_mock):
        server_main()
        instance_mock.assert_called_with()

    @mock.patch('tornado.ioloop.IOLoop.instance')
    def test_pyfreelan_client_launches_an_ioloop(self, instance_mock):
        client_main()
        instance_mock.assert_called_with()