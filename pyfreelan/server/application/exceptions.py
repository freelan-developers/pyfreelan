"""
Exceptions.
"""

from flask import jsonify
from werkzeug.datastructures import WWWAuthenticate


class HTTPException(Exception):
    """
    The base class for all HTTP exceptions.
    """
    status_code = 500
    message = None
    headers = {}

    def __init__(self, message=None, status_code=None, headers=None):
        super(HTTPException, self).__init__()

        if message:
            self.message = message

        if status_code:
            self.status_code = status_code

        if headers:
            self.headers = headers.copy()

    def to_response(self):
        response = jsonify(message=self.message)
        response.status_code = self.status_code
        for key, value in self.headers.iteritems():
            response.headers[key] = value
        return response


def get_basic_auth(realm=None):
    basic_auth = WWWAuthenticate()
    basic_auth.set_basic(realm=realm or 'Authentication required')
    return basic_auth.to_header()


class AuthenticationRequired(HTTPException):
    """
    Authentication is required to access this resource.
    """
    status_code = 401
    message = 'Authentication required.'
    headers = {
        'WWW-Authenticate': get_basic_auth(),
    }


class UnexpectedFormat(HTTPException):
    """
    The request received data in an unexpected format and does not like it very
    much.
    """
    status_code = 406
