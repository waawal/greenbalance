import sys

import tcpforwarder
import wsgibalancer

if __name__ == '__main__':
    import utils
    configuration = utils.process_arguments(sys.argv)
    tcpforwarder.start_server(source=configuration[0], destinations=configuration[1])
