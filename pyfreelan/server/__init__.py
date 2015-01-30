"""
pyfreelan server interface.
"""

from tornado.wsgi import WSGIContainer
from tornado.httpserver import HTTPServer

from .application import APP


class HTTPServer(HTTPServer):
    """
    A HTTP server.
    """

    def __init__(self, configuration):
        """
        Initialize the HTTP server with the specified `configuration`.

        :param configuration: The configuration as given by the FreeLAN core.
        """
        super(HTTPServer, self).__init__(WSGIContainer(APP))

        #TODO: Pick the listen port in the configuration.
        self.listen(12000)
