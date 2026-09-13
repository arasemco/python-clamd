# python-clamd 👋

![GitHub stars](https://img.shields.io/github/stars/arasemco/python-clamd?style=social)
![GitHub forks](https://img.shields.io/github/forks/arasemco/python-clamd?style=social)
![GitHub watchers](https://img.shields.io/github/watchers/arasemco/python-clamd?style=social)
![GitHub repo size](https://img.shields.io/github/repo-size/arasemco/python-clamd)
![GitHub language count](https://img.shields.io/github/languages/count/arasemco/python-clamd)
![GitHub top language](https://img.shields.io/github/languages/top/arasemco/python-clamd)
![GitHub last commit](https://img.shields.io/github/last-commit/arasemco/python-clamd?color=red)
[![Test workflow](https://github.com/arasemco/python-clamd/actions/workflows/main.yml/badge.svg?branch=main)](https://github.com/arasemco/python-clamd/actions/workflows/main.yml)
[![PyPI Version](https://img.shields.io/pypi/v/clamd.svg)](https://pypi.org/project/clamd/)
[![Python Versions](https://img.shields.io/pypi/pyversions/clamd.svg)](https://pypi.org/project/clamd/)

## About

`clamd` is a portable Python module to use the ClamAV anti-virus engine on
Windows, Linux, macOS and other platforms. It requires a running instance of
the `clamd` daemon.

This is a fork of https://github.com/graingert/python-clamd

Original credits:
- pyClamd v0.2.0 by Philippe Lagadec (http://www.decalage.info/en/python/pyclamd)
- pyClamd v0.1.1 by Alexandre Norman (http://xael.org/norman/python/pyclamd/)

## Installation

Install from PyPI:

```bash
pip install clamd
```

Or install from source:

```bash
git clone https://github.com/arasemco/python-clamd.git
cd python-clamd
pip install -e .
```

## Requirements

- Python 3.6 or higher
- Running ClamAV daemon (clamd)

Install ClamAV daemon on Ubuntu:

```bash
sudo apt-get install clamav-daemon clamav-freshclam
sudo freshclam
sudo service clamav-daemon start
```

## Usage

**Unix socket connection**:

```python
>>> import clamd
>>> cd = clamd.ClamdUnixSocket()
>>> cd.ping()
'PONG'
>>> cd.version()
'ClamAV ...'
>>> cd.reload()
'RELOADING'
```

**Network socket connection**:

```python
>>> cd = clamd.ClamdNetworkSocket(host='127.0.0.1', port=3310)
```

**Scan a file**:

```python
>>> with open('/tmp/EICAR', 'wb') as f:
...     f.write(clamd.EICAR)
>>> cd.scan('/tmp/EICAR')
{'/tmp/EICAR': ('FOUND', 'Eicar-Test-Signature')}
```

**Scan a stream (buffer)**:

```python
>>> from io import BytesIO
>>> cd.instream(BytesIO(clamd.EICAR))
{'stream': ('FOUND', 'Eicar-Test-Signature')}
```

**Scan a directory recursively**:

```python
>>> results = cd.multiscan('/path/to/directory')
>>> for path, (status, virus) in results.items():
...     if status == 'FOUND':
...         print(f'Virus found: {virus} in {path}')
```

**Get clamd statistics**:

```python
>>> print(cd.stats())
```

## API Reference

Classes:
- `ClamdUnixSocket(path='/var/run/clamav/clamd.ctl', timeout=None)`
- `ClamdNetworkSocket(host='127.0.0.1', port=3310, timeout=None)`

Both classes derive from the common `BaseClamdSocket` abstract base class.

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

## Testing

The test suite runs against a live `clamd` daemon and is orchestrated with Docker Compose.

Run the full test matrix:

```bash
docker compose run --rm --build python-clamd-test
```

Run against a specific Python version:

```bash
PYTHON_VERSION=3.12 docker compose run --rm --build python-clamd-test
```

Run a single test:

```bash
PYTHON_VERSION=3.12 docker compose run --rm --build python-clamd-test \
    pytest -sv test/test_clamd/test_api.py::TestClamdUnixSocket::test_ping
```

## Development

Start a development container with the source mounted and dependencies installed:

```bash
PYTHON_VERSION=3.12 docker compose run --rm --build python-clamd-dev
```

## License

`clamd` is released as open-source software under the **GNU Lesser General Public License v2.1 or later** (LGPL-2.1-or-later).

## Contributing

Issues and pull requests are welcome at:
https://github.com/arasemco/python-clamd

## Changelog

See [CHANGES.md](CHANGES.md) for version history.