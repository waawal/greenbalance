#!/usr/bin/python

import sys
import signal
import logging
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

def read_config(host=None, port=None, conf=None, loglevel=None, logfile=None):
    """ Reads the configuration file and prepares values for starting up
        the balancer.
    """
    def parse_address(address):
        """ Pareses the hosts and ports in the conf file.
        """
        try:
            hostname, portnumber = address.rsplit(' ', 1)
            portnumber = int(portnumber) # Has to be a INT
        except ValueError:
            sys.exit('Expected HOST PORT: %r' % address)
        return (gethostbyname(hostname), portnumber)

    def setup_logging(logginglevel='error', filename=None):
        """ Sets the right levels and output file from conf-file.
        """
        LEVELS = {'debug':logging.DEBUG,
                  'info':logging.INFO,
                  'warning':logging.WARNING,
                  'error':logging.ERROR,
                  'critical':logging.CRITICAL}
        level = LEVELS.get(logginglevel, logging.NOTSET)
        if filename:
            logging.basicConfig(level=level, filename=filename)
        else:
            logging.basicConfig(level=level)
        
    parser = SafeConfigParser()
    parser.read(conf)
    destinations = {}
    for name, value in parser.items('nodes'):
        key = parse_adress(name)
        destinations[key] = int(value)
    # TODO: Check first if avail! 
    if host == None:
        host = parser.get('settings', 'host') or "0.0.0.0"
    if port == None:
        port = int(parser.get('settings', 'port')) or 8080
    else:
        port = int(port)
    if parser.has_section('logging'):
        if loglevel == None:
            loglevel = parser.get('logging', 'loglevel')
        if logfile == None:
            logfile = parser.get('logging', 'logfile')
        
    # Setup logging
    if loglevel and logfile:
        setup_logging(loglevel, logfile)
    elif loglevel:
        setup_logging(logginglevel=loglevel)
    elif logfile:
        setup_logging(filename=logfile)
    
    return (destinations, (host, port))

def process_arguments(argv=None):
    """ Executes when called from the commandline.
    """
    p = OptionParser(usage="usage: %prog [options] filename",
                          version="%prog 0.2.0")
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
                 help="Configuration File",)
    p.add_option("-l", "--logfile",
                 dest="logfile",
                 default=None,
                 help="Log File",)
    p.add_option("-L", "--loglevel",
                 dest="loglevel",
                 default=None,
                 help="Log Level (debug, info, warning, error, critical)",)
                 
    options, arguments = p.parse_args()
    destinations, source = read_config(options.host, options.port,
                                options.conf, options.loglevel, options.logfile)
    start(source=source, destinations=destinations)

if __name__ == '__main__':
    process_arguments(sys.argv)
