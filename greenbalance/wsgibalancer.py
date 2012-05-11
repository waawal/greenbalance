
import functools
import logging

from gevent import monkey; monkey.patch_all()
from gevent.wsgi import WSGIServer
from wsgiproxy.app import WSGIProxyApp

import distributors
from utils import start
from base import BaseProxy


class WSGIForwarderApp(WSGIProxyApp):

    def __init__(self, destinationsiter):
        WSGIProxyApp.__init__(self, destinationsiter.next())
        self.destinationsiter = destinationsiter

    def __call__(self, environ, start_response):
        self.href__set(self.destinationsiter.next())
        environ = self.encode_environ(environ)
        self.setup_forwarded_environ(environ)
        return self.forward_request(environ, start_response)
        
class WSGIForwarder(BaseProxy):

    def __init__(self, listener=None, destinations=None,
                 distributor=distributors.round_robin, **kwargs):
        if listener == None:
            listener = ('0.0.0.0', 8080)
        BaseProxy.__init__(self, listener=listener,
                               destinations=destinations,
                               distributor=distributor, **kwargs)
        self.server = WSGIServer(listener,
                   application=WSGIForwarderApp(self.get_destination))
        logging.debug('Starting up the WSGI forwarder.')

    def serve_forever(self):
        self.server.serve_forever()

# Aliases & Shortcuts
start_server = functools.partial(start, WSGIForwarder,
                                 distributor=distributors.weighted_random)

