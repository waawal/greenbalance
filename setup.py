#!/usr/bin/python

from distutils.core import setup


with open('README.rst') as file:
    long_description = file.read()

setup(
    data_files = [('', ['README.rst'])],
    name = 'green-balance',
    version = '0.1.0',
    url = 'https://github.com/waawal/green-balance',
    description = 'Weighted Random TCP Loadbalancer.',
    long_description = long_description,
    author = 'Daniel Waardal',
    author_email = 'waawal@boom.ws',
    license = 'gpl',
    platforms = 'any',
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
