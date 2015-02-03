"""
pyfreelan server interface.
"""

from twisted.web.server import Site
from twisted.web.wsgi import WSGIResource
from urlparse import urlparse
from ipaddress import (
    IPv4Address,
    IPv6Address,
)

from .application import APP


def parse_endpoint(endpoint, default_port=0):
    """
    Parses a endpoint string and get its two components.
    :param endpoint: The endpoint string to parse.
    :param default_port: The default port to return in case none was found in
        the parsed `endpoint`.
    :returns: A couple (hostname, port).
    """
    result = urlparse('//{}'.format(endpoint))

    try:
        if endpoint.startswith('['):
            hostname = str(IPv6Address(result.hostname))
        else:
            hostname = str(IPv4Address(result.hostname))
    except ValueError:
        hostname = result.hostname

    port = default_port if result.port is None else result.port

    return hostname, port


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

        hostname, port = parse_endpoint(configuration['listen_on'])
        reactor.listenTCP(port, self.site, interface=hostname)
