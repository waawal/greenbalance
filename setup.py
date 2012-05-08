#!/usr/bin/python

import os
from distutils.core import setup

homedir = os.path.expanduser('~')

with open('README.rst') as file:
    long_description = file.read()

setup(
    data_files = [('', ['README.rst']),
                  ('/etc', ['greenbalance.conf']),],
    name = 'greenbalance',
    version = '0.0.1',
    url = 'https://github.com/waawal/green-balance',
    description = 'Weighted Random Loadbalancer for TCP.',
    long_description = long_description,
    author = 'Daniel Waardal',
    author_email = 'waawal@boom.ws',
    license = 'gpl',
    platforms = 'any',
    scripts=['bin/greenbalance'],
    py_modules = [
        'greenbalance'
    ],
    requires = [
        'wr',
        'gevent'
    ],
    classifiers = [
        'Development Status :: 3 - Alpha',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU General Public License (GPL)',
        'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: System :: Systems Administration',
        'Topic :: Communications',
    ],
)
