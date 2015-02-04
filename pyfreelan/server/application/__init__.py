"""
The Flask application.
"""

from flask import (
    Flask,
    jsonify,
    url_for,
    request,
    g,
    make_response,
)

APP = Flask('pyfreelan')


class UnexpectedFormat(Exception):
    """
    The request received data in an unexpected format and does not like it very
    much.
    """
    status_code = 406

    def __init__(self, message):
        super(UnexpectedFormat, self).__init__()
        self.message = message

    def to_dict(self):
        return {
            'message': self.message,
        }

    def to_response(self):
        response = jsonify(self.to_dict())
        response.status_code = self.status_code
        return response


@APP.errorhandler(UnexpectedFormat)
def handle_unexpected_format(error):
    return error.to_response()


@APP.route('/')
def index():
    return jsonify(
        {
            name: url_for(name)
            for name in {
                'index',
                'request_certificate',
            }
        }
    )


@APP.route('/request_certificate/', methods={'POST'})
def request_certificate():
    try:
        der_certificate = g.http_server.callbacks['sign_certificate_request'](
            der_certificate_request=request.data,
        )
    except ValueError:
        raise UnexpectedFormat(
            "Unable to read the specified certificate request.",
        )

    response = make_response(der_certificate)
    response.mimetype = 'application/x-x509-cert'
    return response
