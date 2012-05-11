
import sys
import functools
import logging

import gevent

from gevent.socket import create_connection, gethostbyname

import distributors
from utils import start
from base import BaseForwarder

import wr

class PortForwarder(BaseForwarder):

    def __init__(self, listener=None, destinations=None,
                 distributor=distributors.round_robin, **kwargs):
        if listener == None:
            listener = ('0.0.0.0', 8080)
        BaseForwarder.__init__(self, listener=listener,
                               destinations=destinations,
                               distributor=distributor, **kwargs)
        logging.debug('Starting up the port forwarder.')

    def handle(self, source, address):
        target = self.get_destination.next()
        try:
            destination = create_connection(target)
        except IOError, ex:
            # TODO: Future implementation of health check.
            logging.error('%s:%s failed to connect to %s:%s: %s' % (address[0],
                          address[1], self.destination[0], self.destination[1],
                          ex))
            return
        
        forwarder = gevent.spawn(self.forward, source, destination)
        backforwarder = gevent.spawn(self.forward, destination, source)
        gevent.joinall([forwarder, backforwarder])

    def forward(self, source, dest):
        """ The Forwarding.
        """
        try:
            while True:
                data = source.recv(1024)
                if not data:
                    break
                dest.sendall(data)
        finally:
            source.close()
            dest.close()

# Aliases & Shortcuts
start_server = functools.partial(start, PortForwarder,
                                distributor=distributors.round_robin)

