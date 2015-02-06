"""
Entry points for pyfreelan.
"""

import os
import logging

from twisted.internet import reactor

from .server import HTTPServer
from .log import LOGGER


def authenticate_user(username, password):
    """
    Authenticate the specified user.

    :param username: The username.
    :param password: The password.
    :returns: :const:`True` if `username` is not empty and matches `password`.

    >>> authenticate_user('alice', 'alice')
    True

    >>> authenticate_user('alice', 'incorrect')
    False

    >>> authenticate_user('', '')
    False
    """
    if username and username == password:
        LOGGER.info("'%s' authentication succeeded.", username)
        return True
    else:
        LOGGER.warning("'%s' authentication failed.", username)
        return False


def server_main():
    """
    The server entry point.
    """
    logging.basicConfig()
    LOGGER.warning(
        "pyfreelan-server is a test HTTP(S) server and is *NOT* suitable for "
        "production use !"
    )
    #TODO: Parse the command line arguments.
    LOGGER.setLevel(logging.DEBUG)
    configuration = {
        'listen_on': '0.0.0.0:12000',
        'secret_key': os.urandom(24),
    }
    callbacks = {
        'authenticate_user': authenticate_user,
    }

    HTTPServer(
        reactor=reactor,
        configuration=configuration,
        callbacks=callbacks,
    )
    reactor.run()


def client_main():
    """
    The client entry point.
    """
    logging.basicConfig()
    reactor.run()
