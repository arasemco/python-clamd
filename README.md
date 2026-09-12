# python-clamd 👋

![GitHub stars](https://img.shields.io/github/stars/arasemco/python-clamd?style=social)
![GitHub forks](https://img.shields.io/github/forks/arasemco/python-clamd?style=social)
![GitHub watchers](https://img.shields.io/github/watchers/arasemco/python-clamd?style=social)
![GitHub repo size](https://img.shields.io/github/repo-size/arasemco/python-clamd)
![GitHub language count](https://img.shields.io/github/languages/count/arasemco/python-clamd)
![GitHub top language](https://img.shields.io/github/languages/top/arasemco/python-clamd)
![GitHub last commit](https://img.shields.io/github/last-commit/arasemco/python-clamd?color=red)

clamd
=====

.. image:: https://github.com/arasemco/python-clamd/workflows/Test/badge.svg?branch=master
   :alt: GitHub Actions build status
   :target: https://github.com/arasemco/python-clamd/actions

.. image:: https://img.shields.io/pypi/v/clamd.svg
   :alt: PyPI Version
   :target: https://pypi.org/project/clamd/

.. image:: https://img.shields.io/pypi/pyversions/clamd.svg
   :alt: Python Versions
   :target: https://pypi.org/project/clamd/

About
-----

`clamd` is a portable Python module to use the ClamAV anti-virus engine on
Windows, Linux, macOS and other platforms. It requires a running instance of
the `clamd` daemon.

This is a fork from https://github.com/graingert/python-clamd

Original credits:
- pyClamd v0.2.0 by Philippe Lagadec (http://www.decalage.info/en/python/pyclamd)
- pyClamd v0.1.1 by Alexandre Norman (http://xael.org/norman/python/pyclamd/)

Installation
------------

Install from PyPI::

    pip install clamd

Or install from source::

    git clone https://github.com/arasemco/python-clamd.git
    cd python-clamd
    pip install -e .

Requirements
------------

- Python 3.9 or higher
- Running ClamAV daemon (clamd)

Install ClamAV daemon on Ubuntu::

    sudo apt-get install clamav-daemon clamav-freshclam
    sudo freshclam
    sudo service clamav-daemon start

Usage
-----

**Unix socket connection**::

    >>> import clamd
    >>> cd = clamd.ClamdUnixSocket()
    >>> cd.ping()
    'PONG'
    >>> cd.version()
    'ClamAV ...'
    >>> cd.reload()
    'RELOADING'

**Network socket connection**::

    >>> cd = clamd.ClamdNetworkSocket(host='127.0.0.1', port=3310)

**Scan a file**::

    >>> with open('/tmp/EICAR', 'wb') as f:
    ...     f.write(clamd.EICAR)
    >>> cd.scan('/tmp/EICAR')
    {'/tmp/EICAR': ('FOUND', 'Eicar-Test-Signature')}

**Scan a stream (buffer)**::

    >>> from io import BytesIO
    >>> cd.instream(BytesIO(clamd.EICAR))
    {'stream': ('FOUND', 'Eicar-Test-Signature')}

**Scan a directory recursively**::

    >>> results = cd.multiscan('/path/to/directory')
    >>> for path, (status, virus) in results.items():
    ...     if status == 'FOUND':
    ...         print(f'Virus found: {virus} in {path}')

**Get clamd statistics**::

    >>> print(cd.stats())

API Reference
-------------

Classes:
- `ClamdUnixSocket(path='/var/run/clamav/clamd.ctl', timeout=None)`
- `ClamdNetworkSocket(host='127.0.0.1', port=3310, timeout=None)`

Methods:
- `ping()` - Check if clamd is responding
- `version()` - Get clamd version
- `reload()` - Reload virus definitions
- `scan(file)` - Scan a single file
- `contscan(file)` - Continuous scan (don't stop on error)
- `multiscan(file)` - Multi-threaded directory scan
- `instream(buffer)` - Scan a byte stream
- `stats()` - Get clamd statistics
- `shutdown()` - Shutdown clamd daemon

Exceptions:
- `ConnectionError` - Connection to clamd failed
- `ResponseError` - Invalid response from clamd
- `BufferTooLongError` - Stream exceeds max length

Testing
-------

Run tests with tox::

    tox

Run specific Python version::

    tox -e py312

Run single test::

    tox -e py312 -- src/tests/test_api.py::TestUnixSocket::test_ping

Development
-----------

Install development dependencies::

    pip install -e .[dev]

Run linting::

    tox -e lint

License
-------

`clamd` is released as open-source software under the **GNU Lesser General Public License v2.1 or later** (LGPL-2.1-or-later).

Contributing
------------

Issues and pull requests are welcome at:
https://github.com/arasemco/python-clamd

Changelog
---------

See `CHANGES.rst` for version history.
