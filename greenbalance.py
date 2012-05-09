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
        target = self.get_destination()
        destination = create_connection(target)
        forwarder = gevent.spawn(self.forward, source, destination)
        backforwarder = gevent.spawn(self.forward, destination, source)
        gevent.joinall([forwarder, backforwarder])

    def close(self):
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

def start(source, destinations):
    """ Registers signals and sets the gevent StreamServer to serve_forever.
    """
    server = PortForwarder(source, destinations)
    gevent.signal(signal.SIGTERM, server.close)
    gevent.signal(signal.SIGQUIT, server.close)
    gevent.signal(signal.SIGINT, server.close)
    server.serve_forever()

def read_config(host=None, port=None, conf=None):
    """ Reads the configuration file and prepares values for starting up
        the balancer.
    """
    def parse_address(address):
        """ Pareses the hosts and ports in the conf file (splits on first space).
        """
        try:
            hostname, portnumber = address.rsplit(' ', 1)
            portnumber = int(portnumber) # Has to be a INT
        except ValueError:
            sys.exit('Expected HOST PORT: %r' % address)
        return (gethostbyname(hostname), portnumber)

    parser = SafeConfigParser()
    parser.read(conf)
    destinations = {}
    for name, value in parser.items('nodes'):
        key = parse_adress(name)
        destinations[key] = int(value)
    if host == None:
        host = parser.get('settings', 'host') or "0.0.0.0"
    if port == None:
        port = int(parser.get('settings', 'port')) or 8080
    else:
        port = int(port)
    
    return (destinations, (host, port))

def process_arguments(argv=None):
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
    nodes, source = read_configoptions.host, options.port, options.conf)
    start(source, destinations)

if __name__ == '__main__':
    process_arguments(sys.argv)
