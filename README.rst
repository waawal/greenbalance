.. image:: http://farm7.staticflickr.com/6193/6049536620_7668b16abf_z.jpg
    :alt: http://www.flickr.com/photos/fincher69/6049536620/
    :target: http://pypi.python.org/pypi/green-balance

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

License
-------
`GPL <http://www.gnu.org/licenses/gpl-3.0.txt>`_
