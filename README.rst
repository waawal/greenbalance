.. image:: http://farm4.staticflickr.com/3043/2343360380_fdbd835cff_t.jpg
    :alt: http://www.flickr.com/photos/gorupka/2343360380/
    :align: right
    :target: http://www.flickr.com/photos/gorupka/2343360380/

greenbalance
============

*greenbalance is a simple TCP load balancer with round-robin and weighted random support built on* ``gevent`` *and* ``wr``.

Usage
=====

Simple example; this will make the load balancer listen on port 8080 and use a custom configuration.
::

    $ greenbalance --port 8080 --config /path/to/my.config

Arguments
---------
Arguments accepted by the ``greenbalance`` command.

--version
  Show program's version number and exit.
-h, --help
  Show this help message and exit.
-H, --host
  IP or Hostname.
-p, --port
  Listening Port.
-c, --config
  Configuration file.


Example greenbalance.conf
-------------------------

``greenbalance.conf`` is by default placed in ``/etc`` if the package was intalled with root privileges. If you have the package installed in a virtualenv you will have to create a configuration file manually and pass it with the ``--config`` or ``-c`` argument.

::

    [settings]
    host = 0.0.0.0           # Bind to this (0.0.0.0 = all)
    port = 3001              # Listening port.

    [nodes]
    backend1 3101 = 20       # will serve 20% of the requests.
    192.168.100.7 3102 = 40  # will serve 40% of the requests.
    localhost 3103 = 40      # will serve 40% of the requests.

Installation
============

*See blow for OS-specific preparations.*

Install *greenbalance* with ``sudo pip install greenbalance``

Ubuntu
------

``sudo apt-get install python-pip python-gevent; sudo pip install --upgrade pip``

CentOS
------

Install ``python-pip`` and ``python-gevent`` from ``epel``.

Documentation
=============

Documentation is available at `readthedocs.org <http://greenbalance.readthedocs.org/>`_

License
=======
`GPL <http://www.gnu.org/licenses/gpl-3.0.txt>`_
