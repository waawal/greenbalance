.. image:: http://farm7.staticflickr.com/6193/6049536620_7668b16abf_z.jpg
    :alt: http://www.flickr.com/photos/fincher69/6049536620/
    :target: http://pypi.python.org/pypi/green-balance

greenbalance
=============

*greenbalance is a TCP loadbalancer built with gevent and wr*



Example greenbalance.conf
-------------------------
::

    [settings]
    host = 0.0.0.0
    port = 3001

    [nodes]
    localhost 3101 = 20
    localhost 3102 = 40
    localhost 3102 = 40

Installation
-----------------------------

Install greenbalance with ``pip install greenbalance``

License
-------
`GPL <http://www.gnu.org/licenses/gpl-3.0.txt>`_
