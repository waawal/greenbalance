.. image:: http://farm4.staticflickr.com/3043/2343360380_fdbd835cff_t.jpg
    :alt: http://www.flickr.com/photos/gorupka/2343360380/
    :align: right
    :target: http://www.flickr.com/photos/gorupka/2343360380/

greenbalance
=============

*greenbalance is a TCP loadbalancer with round-robin and weighted random support built on gevent and wr*

``greenbalance.conf`` is by default installed to ``/etc/greenbalance.conf``

Usage
-----
::

    $ greenbalance --port 8080 --config /path/to/my.config

Example greenbalance.conf
-------------------------
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

* Ubuntu: ``sudo apt-get install python-pip python-gevent; sudo pip install --upgrade pip``

Install greenbalance with ``sudo pip install greenbalance``  
*sudo is needed because the configuration file will be written to /etc*

Documentation
-------------

Documentation is available at `readthedocs.org <http://greenbalance.readthedocs.org/>`_

License
-------
`GPL <http://www.gnu.org/licenses/gpl-3.0.txt>`_
