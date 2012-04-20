import sys
import signal
import gevent
from gevent.server import StreamServer
from gevent.socket import create_connection, gethostbyname
import wr

destinationsdict = {
(gethostbyname('localhost'), 3101): 1,
(gethostbyname('localhost'), 3102): 1,
}

def append_x_headers(source, data):
    print type(data)
    print data
    #xforwardedfor= ''.join(("X-Forwarded-For: ", source.getpeername()[0], "\n"))
    #return '\n'.join(list(data.split("\n")[0], xforwardedfor,
    #                  *data.split("\n")[1:]
    #                  ))

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
        print 'Closing listener socket'
        StreamServer.close(self)

    @property
    def dest(self):
        return wr.choice(self.destinations)


def forward(source, dest):
    source_address = '%s:%s' % source.getpeername()[:2]
    dest_address = '%s:%s' % dest.getpeername()[:2]
    log('[Relaying] %s->%s', source_address, dest_address)
    try:
        while True:
            data = source.recv(1024)
            if not data:
                break
            append_x_headers(source, data)
            dest.sendall(data)
            
    finally:
        source.close()
        dest.close()


def parse_address(address):
    try:
        hostname, port = address.rsplit(':', 1)
        port = int(port)
    except ValueError:
        sys.exit('Expected HOST:PORT: %r' % address)
    return gethostbyname(hostname), port


def main():
    #args = sys.argv[1:]
    #if len(args) != 2:
    #    sys.exit('Usage: %s source-address destination-address' % __file__)
    source = parse_address("0.0.0.0:3001")
    #dest = parse_address(args[1])
    server = PortForwarder(source, destinationsdict)
    #log('Starting port forwarder %s:%s -> %s:%s', *(server.address[:2] + dest))
    gevent.signal(signal.SIGTERM, server.close)
    gevent.signal(signal.SIGQUIT, server.close)
    gevent.signal(signal.SIGINT, server.close)
    server.serve_forever()


def log(message, *args):
    message = message % args
    sys.stderr.write(message + '\n')


if __name__ == '__main__':
    main()
