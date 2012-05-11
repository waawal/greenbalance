#!/usr/bin/python

import sys
import signal

import gevent
from gevent.server import StreamServer
from gevent.socket import create_connection, gethostbyname

import wr

class PortForwarder(StreamServer):

    def __init__(self, listener, destinations, **kwargs):
        StreamServer.__init__(self, listener, **kwargs)
        self.destinations = destinations
        logging.debug('Starting up the port forwarder.')

    def handle(self, source, address):
        target = self.get_destination()
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

    def close(self):
        if self.closed:
            logging.critical('Multiple exit signals received - aborting.')
            sys.exit('Multiple exit signals received - aborting.')
        else:
            StreamServer.close(self)

    def get_destination(self):
        destination = wr.choice(self.destinations)
        return destination

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

def start(destinations, source=None):
    """ Registers signals, instantiates and sets the gevent StreamServer
        to serve_forever.
    """
    if source == None:
        source = ("0.0.0.0", 8080)
    server = PortForwarder(source, destinations)
    gevent.signal(signal.SIGTERM, server.close)
    gevent.signal(signal.SIGINT, server.close)
    server.serve_forever()

if __name__ == '__main__':
    import utils
    utils.process_arguments(sys.argv)
