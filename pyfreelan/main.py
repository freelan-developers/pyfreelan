"""
Entry points for pyfreelan.
"""

import logging

from twisted.internet import reactor

from .server import HTTPServer

LOGGER = logging.getLogger(__name__)


def server_main():
    """
    The server entry point.
    """
    logging.basicConfig()
    configuration = {}

    HTTPServer(reactor=reactor, configuration=configuration)
    reactor.run()


def client_main():
    """
    The client entry point.
    """
    logging.basicConfig()
    reactor.run()
