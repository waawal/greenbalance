#!/usr/bin/python

import sys
import signal
from optparse import OptionParser
from ConfigParser import SafeConfigParser

import gevent
from gevent.server import StreamServer
from gevent.socket import create_connection, gethostbyname

import wr


class PortForwarder(StreamServer):

    def __init__(self, listener, destinations, **kwargs):
        StreamServer.__init__(self, listener, **kwargs)
        self.destinations = destinations

    def handle(self, source, address):
        dest = create_connection(self.dest)
        forwarder = gevent.spawn(forward, source, dest)
        backforwarder = gevent.spawn(forward, dest, source)
        gevent.joinall([forwarder, backforwarder])

    def close(self):
        StreamServer.close(self)

    @property
    def dest(self):
        return parse_address(wr.choice(self.destinations))


def forward(source, dest):
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

def parse_address(address):
    """ Pareses the hosts and ports in the conf file (splits on first space).
    """
    try:
        hostname, port = address.rsplit(' ', 1)
        port = int(port)
    except ValueError:
        sys.exit('Expected HOST PORT: %r' % address)
    return gethostbyname(hostname), port

def read_config(host=None, port=None, conf=None):
    parser = SafeConfigParser()
    parser.read(conf)
    destinationsdict = {}
    for name, value in parser.items('nodes'):
        destinationsdict[name] = int(value)
    if not host:
        host = parser.get('settings', 'host')
    if not port:
        port = int(parser.get('settings', 'port'))
    else:
        port = int(port)
    
    return destinationsdict, (host, port)

def start(host=None, port=None, conf=None):
    """ Registers signals and sets the gevent StreamServer to serve_forever.
    """
    nodes, source = read_config(host, port, conf)
    server = PortForwarder(source, nodes)
    gevent.signal(signal.SIGTERM, server.close)
    gevent.signal(signal.SIGQUIT, server.close)
    gevent.signal(signal.SIGINT, server.close)
    server.serve_forever()

def main(argv):
    """ Executes when called from the commandline.
    """
    p = OptionParser(usage="usage: %prog [options] filename",
                          version="%prog 0.1.0")
    p.add_option("-H", "--host",
                 dest="host",
                 default=None,
                 help="IP or Hostname")
    p.add_option("-p", "--port",
                 dest="port",
                 default=None,
                 help="Listening Port",)
    p.add_option("-c", "--config",
                 dest="conf",
                 default="/etc/greenbalance.conf",
                 help="Configuration file",)
    options, arguments = p.parse_args()
    start(options.host, options.port, options.conf)

if __name__ == '__main__':
    main(sys.argv)
