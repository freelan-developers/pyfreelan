"""
pyfreelan server interface.
"""

from twisted.web.server import Site
from twisted.web.wsgi import WSGIResource

from .application import APP


class HTTPServer(object):
    """
    A HTTP server.
    """

    def __init__(self, reactor, configuration):
        """
        Initialize the HTTP server with the specified `configuration`.

        :param reactor: The reactor to bind to.
        :param configuration: The configuration as given by the FreeLAN core.
        """
        self.resource = WSGIResource(reactor, reactor.getThreadPool(), APP)
        self.site = Site(self.resource)
        #TODO: Pick the listen port in the configuration.
        reactor.listenTCP(12000, self.site, interface="0.0.0.0")
