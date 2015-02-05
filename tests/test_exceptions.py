"""
Test the exceptions.
"""

import json

from unittest import TestCase

from pyfreelan.server.application import APP
from pyfreelan.server.application.exceptions import HTTPException


class ExceptionTests(TestCase):
    def setUp(self):
        self.app = APP

    def test_http_exception_translates_to_response(self):
        message = 'Some error'
        status_code = 404
        headers = {'a': '1', 'b': '2'}

        ex = HTTPException(
            message=message,
            status_code=status_code,
            headers=headers,
        )

        self.assertEqual(message, ex.message)
        self.assertEqual(status_code, ex.status_code)
        self.assertEqual(headers, ex.headers)

        with self.app.test_request_context():
            response = ex.to_response()

            self.assertEqual({'message': message}, json.loads(response.data))
            self.assertEqual(status_code, response.status_code)

            for key, value in headers.iteritems():
                self.assertEqual(value, response.headers.get(key))
