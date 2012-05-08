.. image:: http://farm4.staticflickr.com/3043/2343360380_fdbd835cff_t.jpg
    :alt: http://www.flickr.com/photos/gorupka/2343360380/
    :align: right
    :target: http://www.flickr.com/photos/gorupka/2343360380/

greenbalance
=============

*greenbalance is a simple TCP loadbalancer with round-robin and weighted random support built on* ``gevent`` *and* ``wr``*.*

Usage
-----

Simple example; this will make the loadbalancer listen on port 8080 and use a custom configuration.
::

    $ greenbalance --port 8080 --config /path/to/my.config

Get all commandline options by:
::

    $ greenbalance -h
    Usage: greenbalance [options] filename
    
    Options:
      --version               Show program's version number and exit
      -h, --help              Show this help message and exit
      -H HOST, --host=HOST    IP or Hostname
      -p PORT, --port=PORT    Listening Port
      -c CONF, --config=CONF  Configuration file


Example greenbalance.conf
-------------------------

``greenbalance.conf`` is by default installed to ``/etc/greenbalance.conf``

::

    [settings]
    host = 0.0.0.0           # Bind to this (0.0.0.0 = all)
    port = 3001              # Listening port.

    [nodes]
    backend1 3101 = 20       # will serve 20% of the requests.
    192.168.100.7 3102 = 40  # will serve 40% of the requests.
    localhost 3103 = 40      # will serve 40% of the requests.

Installation
------------

* **Ubuntu:** ``sudo apt-get install python-pip python-gevent; sudo pip install --upgrade pip``
* **CentOS:** Install ``python-pip`` and ``python-gevent`` from ``epel``.

Install greenbalance with ``sudo pip install greenbalance``  
*sudo is needed because the configuration file will be written to /etc*

Documentation
-------------

Documentation is available at `readthedocs.org <http://greenbalance.readthedocs.org/>`_

License
-------
`GPL <http://www.gnu.org/licenses/gpl-3.0.txt>`_
