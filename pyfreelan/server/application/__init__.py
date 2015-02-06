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
from flask.ext.login import (
    login_required,
    current_user,
)
from functools import wraps

from .security import LOGIN_MANAGER
from .exceptions import (
    HTTPException,
    UnexpectedFormat,
)
from ...log import LOGGER

APP = Flask('pyfreelan')
LOGIN_MANAGER.init_app(APP)


def log_activity(func):
    """
    Log any activity of the decorated request.

    :param func: The function to decorate.
    :returns: The decorated function.
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        LOGGER.debug(
            "Web request from '%s' to '%s' (%s).",
            current_user.get_id(),
            request.url,
            request.method,
        )

        response = func(*args, **kwargs)

        LOGGER.debug(
            "Web response to '%s' from '%s': %s\n%s",
            current_user.get_id(),
            request.url,
            response.status,
            response.data,
        )
        return response

    return wrapper


@APP.errorhandler(HTTPException)
def handle_unexpected_format(error):
    return error.to_response()


@APP.route('/')
@log_activity
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
@log_activity
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
