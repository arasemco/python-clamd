#!/usr/bin/env python
from pathlib import Path

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as f:
    readme = f.read()

with open("CHANGES.md", "r", encoding="utf-8") as f:
    history = f.read()

with open("requirements.txt", "r", encoding="utf-8") as f:
    install_requires = f.readlines()

extras_require = {}
extras_requirements = Path(__file__).parent
for requirements in extras_requirements.glob("requirements-*.txt"):
    with open(requirements, "r", encoding="utf-8") as f:
        extras_require[requirements.stem.split("-")[1]] = f.readlines()

setup(
    name="clamd",
    version="1.0.3",
    author="Aram Semo",
    author_email="aram.semo@asemo.pro",
    maintainer="Aram Semo",
    maintainer_email="aram.semo@asemo.pro",

    install_requires=install_requires,
    extras_require=extras_require,

    package_dir={"clamd": "src/clamd"},
    packages=find_packages(where="src"),
    python_requires=">=3.6",

    license="LGPL-2.1-or-later",
    url="https://github.com/arasemco/python-clamd",
    project_urls={
        "Homepage": "https://github.com/arasemco/python-clamd",
        "Repository": "https://github.com/arasemco/python-clamd.git",
        "Original-pyClamd": "https://xael.org/norman/python/pyclamd/",
        "Improved-pyClamd": "https://www.decalage.info/en/python/pyclamd",
    },
    keywords=["python", "clamav", "antivirus", "scanner", "virus", "libclamav", "clamd"],
    description="Python client for ClamAV clamd",
    long_description=readme + "\n\n" + history,
    long_description_content_type="text/markdown",
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: GNU Library General Public License v2 or later (LGPLv2+)",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Programming Language :: Python :: 3.13",
        "Programming Language :: Python :: 3.14",
        "Topic :: Security",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: System :: Monitoring",
    ],
)
