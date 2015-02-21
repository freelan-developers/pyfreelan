"""
Tests web server views.
"""

import json
import mock
import dateutil.parser

from datetime import datetime
from unittest import TestCase
from contextlib import contextmanager
from base64 import b64encode
from functools import wraps
from flask import g
from flask.testing import FlaskClient

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
    def with_credentials(self, result):
        username = 'user1'
        password = 'password'
        authentication_headers = {
            'Authorization': 'Basic {}'.format(
                b64encode('{username}:{password}'.format(
                    username=username,
                    password=password,
                )),
            ),
        }

        def authenticate_user(*args, **kwargs):
            return result

        @contextmanager
        def patch_method(method):
            original_method = getattr(FlaskClient, method)

            @wraps(original_method)
            def wrapper(*args, **kwargs):
                headers = kwargs.setdefault('headers', {})
                headers.update(authentication_headers)
                return original_method(*args, **kwargs)

            with mock.patch(
                'flask.testing.FlaskClient.{}'.format(method),
                wrapper,
            ) as mocked:
                yield mocked

        @contextmanager
        def patch_methods(methods):
            if methods:
                with patch_method(methods[0]), patch_methods(methods[1:]):
                    yield
            else:
                yield

        methods = ['get', 'post', 'put', 'delete']

        with self.register_callback(authenticate_user), patch_methods(methods):
            yield result

    def test_index(self):
        indexes = {
            'index',
            'request_certificate',
        }

        with self.with_credentials(True):
            response = self.client.get('/')

        self.assertEqual(200, response.status_code)
        self.assertEqual('application/json', response.content_type)
        self.assertEqual(indexes, set(json.loads(response.data)))

    def test_index_with_existing_session(self):
        with self.with_credentials(True):
            response = self.client.get('/')
            self.assertEqual(200, response.status_code)

        with self.with_credentials(False):
            response = self.client.get('/')
            self.assertEqual(200, response.status_code)

    def test_index_without_credentials(self):
        response = self.client.get('/')
        self.assertEqual(401, response.status_code)
        self.assertEqual('application/json', response.content_type)

    def test_index_with_invalid_credentials(self):
        with self.with_credentials(False):
            response = self.client.get('/')

        self.assertEqual(401, response.status_code)
        self.assertEqual('application/json', response.content_type)

    def test_request_certificate(self):
        der_certificate_request = 'der_certificate_request'
        der_certificate = 'der_certificate'

        def sign_certificate_request(der_certificate_request):
            if der_certificate_request:
                return der_certificate

        with self.with_credentials(True), \
                self.register_callback(sign_certificate_request):
            response = self.client.post(
                '/request_certificate/',
                data=der_certificate_request,
            )

        self.assertEqual(200, response.status_code)
        self.assertEqual('application/x-x509-cert', response.content_type)
        self.assertEqual(der_certificate, response.data)

    def test_request_certificate_failure_returns_406(self):
        der_certificate_request = 'der_certificate_request'

        def sign_certificate_request(der_certificate_request):
            raise ValueError

        with self.with_credentials(True), \
                self.register_callback(sign_certificate_request):
            response = self.client.post(
                '/request_certificate/',
                data=der_certificate_request,
            )

        self.assertEqual(406, response.status_code)
        self.assertEqual('application/json', response.content_type)
        self.assertIn('message', set(json.loads(response.data)))

    def test_request_ca_certificate(self):
        der_ca_certificate = 'der_ca_certificate'

        def get_ca_certificate():
            return der_ca_certificate

        with self.with_credentials(True), \
                self.register_callback(get_ca_certificate):
            response = self.client.get(
                '/request_ca_certificate/',
            )

        self.assertEqual(200, response.status_code)
        self.assertEqual('application/x-x509-cert', response.content_type)
        self.assertIn(der_ca_certificate, response.data)

    def test_register(self):
        now = datetime.now()
        der_certificate = 'der_certificate'

        def register(der_certificate):
            return {
                'expiration_timestamp': now,
            }

        with self.with_credentials(True), self.register_callback(register):
            response = self.client.post(
                '/register/',
                data=der_certificate,
            )

        self.assertEqual(200, response.status_code)
        self.assertEqual('application/json', response.content_type)

        registration = json.loads(response.data)
        print registration
        expiration_timestamp = dateutil.parser.parse(
            registration['expiration_timestamp'],
        )
        self.assertEqual(expiration_timestamp, now)

    def test_register_failure_returns_406(self):
        der_certificate = 'der_certificate'

        def register(der_certificate):
            raise ValueError

        with self.with_credentials(True), self.register_callback(register):
            response = self.client.post(
                '/register/',
                data=der_certificate,
            )

        self.assertEqual(406, response.status_code)
        self.assertEqual('application/json', response.content_type)
        self.assertIn('message', set(json.loads(response.data)))

    def test_unregister(self):
        def unregister():
            pass

        with self.with_credentials(True), self.register_callback(unregister):
            response = self.client.post(
                '/unregister/',
            )

        self.assertEqual(204, response.status_code)
