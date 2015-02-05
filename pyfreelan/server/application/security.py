"""
Security-related functions.
"""

from flask import g
from flask.ext.login import (
    LoginManager,
    login_user,
)

from .user import User
from .exceptions import AuthenticationRequired

LOGIN_MANAGER = LoginManager()


@LOGIN_MANAGER.user_loader
def load_user(username):
    return User(username=username)


@LOGIN_MANAGER.unauthorized_handler
def unauthorized():
    raise AuthenticationRequired


@LOGIN_MANAGER.request_loader
def load_user_from_request(request):
    if request.authorization:
        username = request.authorization.username
        password = request.authorization.password

        if g.http_server.callbacks['authenticate_user'](username, password):
            user = User(
                username=request.authorization.username,
            )
            login_user(user)

            return user
