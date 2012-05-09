#!/usr/bin/python

import os
import os.path
from distutils.core import setup

datafiles = [('', ['README.rst'])]
homedir = os.path.expanduser('~')

if os.access('/etc', os.W_OK) and not os.path.exists(os.path.join('/etc', 'greenbalance.conf')):
    datafiles.append(('/etc', ['greenbalance.conf']))

with open('README.rst') as file:
    long_description = file.read()

setup(
    data_files = datafiles,
    name = 'greenbalance',
    version = '0.1.0',
    url = 'https://github.com/waawal/greenbalance',
    description = 'Weighted Random Load Balancer for TCP.',
    long_description = long_description,
    author = 'Daniel Waardal',
    author_email = 'waawal@boom.ws',
    license = 'gpl',
    platforms = 'any',
    scripts=['bin/greenbalance'],
    py_modules = [
        'greenbalance'
    ],
    install_requires = [
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
