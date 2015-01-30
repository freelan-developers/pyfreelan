"""
Entry points for pyfreelan.
"""

from tornado.ioloop import IOLoop

from .server import HTTPServer


def server_main():
    """
    The server entry point.
    """
    configuration = {}

    HTTPServer(configuration=configuration)
    IOLoop.instance().start()


def client_main():
    """
    The client entry point.
    """
    pass
