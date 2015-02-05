"""
Tests web server views.
"""

import json
import mock

from unittest import TestCase
from contextlib import contextmanager
from base64 import b64encode
from flask import g

from pyfreelan.server.application import APP


class WebServerViewsTests(TestCase):
    def setUp(self):
        self.app = APP
        self.client = self.app.test_client()
        self.http_server = mock.MagicMock()
        self.http_server.callbacks = {}

        @self.app.before_request
        def register_mock_http_server():
            g.http_server = self.http_server

    @contextmanager
    def register_callback(self, callback, name=None):
        if not name:
            name = callback.__name__

        with mock.patch.dict(self.http_server.callbacks, **{name: callback}):
            yield

    @contextmanager
    def enable_credentials(self, result):
        username = 'user1'
        password = 'password'

        def authenticate_user(*args, **kwargs):
            return result

        with self.register_callback(authenticate_user):
            yield self.get_credentials(username, password)

    def get_credentials(self, username, password):
        return {
            'Authorization': 'Basic {}'.format(
                b64encode('{username}:{password}'.format(
                    username=username,
                    password=password,
                )),
            ),
        }

    def test_index(self):
        indexes = {
            'index',
            'request_certificate',
        }

        with self.enable_credentials(True) as credentials:
            response = self.client.get('/', headers=credentials)

        self.assertEqual(200, response.status_code)
        self.assertEqual('application/json', response.content_type)
        self.assertEqual(indexes, set(json.loads(response.data)))

    def test_index_with_existing_session(self):
        with self.enable_credentials(True) as credentials:
            response = self.client.get('/', headers=credentials)
            self.assertEqual(200, response.status_code)

            response = self.client.get('/')
            self.assertEqual(200, response.status_code)

    def test_index_without_credentials(self):
        response = self.client.get('/')
        self.assertEqual(401, response.status_code)
        self.assertEqual('application/json', response.content_type)

    def test_index_with_invalid_credentials(self):
        with self.enable_credentials(False) as credentials:
            response = self.client.get('/', headers=credentials)

        self.assertEqual(401, response.status_code)
        self.assertEqual('application/json', response.content_type)

    def test_request_certificate(self):
        der_certificate_request = 'der_certificate_request'
        der_certificate = 'der_certificate'

        def sign_certificate_request(der_certificate_request):
            if der_certificate_request:
                return der_certificate

        with self.enable_credentials(True) as credentials:
            with self.register_callback(sign_certificate_request):
                response = self.client.post(
                    '/request_certificate/',
                    data=der_certificate_request,
                    headers=credentials,
                )

        self.assertEqual(200, response.status_code)
        self.assertEqual('application/x-x509-cert', response.content_type)
        self.assertEqual(der_certificate, response.data)

    def test_request_certificate_failure_returns_406(self):
        der_certificate_request = 'der_certificate_request'

        def sign_certificate_request(der_certificate_request):
            raise ValueError

        with self.enable_credentials(True) as credentials:
            with self.register_callback(sign_certificate_request):
                response = self.client.post(
                    '/request_certificate/',
                    data=der_certificate_request,
                    headers=credentials,
                )

        self.assertEqual(406, response.status_code)
        self.assertEqual('application/json', response.content_type)
        self.assertIn('message', set(json.loads(response.data)))
