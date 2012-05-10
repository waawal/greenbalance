#!/usr/bin/python

import os
import os.path
from distutils.core import setup

datafiles = [('', ['README.rst'])]
homedir = os.path.expanduser('~')

if os.access('/etc', os.W_OK) and not os.path.exists(os.path.join('/etc', 'greenbalance.conf')):
    datafiles.append(('/etc', ['conf/greenbalance.conf']))

with open('README.rst') as file:
    long_description = file.read()

setup(
    data_files = datafiles,
    name = 'greenbalance',
    version = '0.2.0',
    url = 'https://github.com/waawal/greenbalance',
    description = 'Load Balancer for TCP.',
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
        'Intended Audience :: System Administrators',
        'License :: OSI Approved :: GNU General Public License (GPL)',
        'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Topic :: Internet',
        'Topic :: System :: Systems Administration',
        'Topic :: Communications',
    ],
)
