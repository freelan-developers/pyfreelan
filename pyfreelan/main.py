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
    #TODO: Parse the command line arguments.
    configuration = {
        'listen_on': '0.0.0.0:12000',
    }
    callbacks = {}

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
