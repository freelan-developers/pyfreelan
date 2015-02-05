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
from flask.ext.login import login_required

from .security import LOGIN_MANAGER
from .exceptions import (
    HTTPException,
    UnexpectedFormat,
)

APP = Flask('pyfreelan')
LOGIN_MANAGER.init_app(APP)


@APP.errorhandler(HTTPException)
def handle_unexpected_format(error):
    return error.to_response()


@APP.route('/')
@login_required
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
@login_required
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
