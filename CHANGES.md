Changes
=========

1.0.3 (unreleased)
------------------

- Introduced `BaseClamdSocket`, a common abstract base class for `ClamdNetworkSocket` and `ClamdUnixSocket`, replacing the previous inheritance of `ClamdUnixSocket` from `ClamdNetworkSocket`.
- Added type hints throughout the public API.
- Resolved `__version__` via `importlib.metadata` on Python 3.8+, falling back to `pkg_resources` on older versions.
- Converted documentation from reStructuredText to Markdown (`README.rst` -> `README.md`, `CHANGES.rst` -> `CHANGES.md`).
- Replaced Travis CI and tox with GitHub Actions and pytest, running against a live ClamAV daemon via Docker Compose across a matrix of Python versions (3.6-3.14).
- Moved the test suite from `src/tests` to `test/`, with fixtures shared through `test/conftest.py`.
- Removed `ez_setup.py`, `setup.cfg`, `tox.ini`, and `MANIFEST.in`; rewrote `setup.py` to read dependencies and metadata from the new project layout.
- Dropped support for Python 2 (removed `from __future__ import unicode_literals`).


1.0.2 (2014-08-21)
------------------

- Remove all dependencies. clamd is now standalone!
- Use plain setuptools no d2to1.
- Create universal wheel.


1.0.1 (2013-03-06)
------------------

- Updated d2to1 dependency


1.0.0 (2013-02-08)
------------------

- Change public interface, including exceptions
- Support Python 3.3, withdraw 2.5 support


0.3.4 (2013-02-01)
------------------

- Use regex to parse file status reponse instead of complicated string split/join


0.3.3 (2013-01-28)
------------------

- First version of clamd that can be installed from PyPI
