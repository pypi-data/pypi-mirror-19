#!/usr/bin/env python3

from distutils.core import setup

name     = "gog-install"
base_url = "http://chadok.info/gog-install"
version  = "0.1.0"

with open('README.txt') as file:
    long_description = file.read()

setup(
    name         = name,
    version      = version,
    description  = "Install GOG.com games from .sh archives",
    long_description = long_description,
    author       = "Olivier Schwander",
    author_email = "olivier.schwander@chadok.info",
    url          = base_url,
    download_url = base_url + "/" + name + "-" + version + ".tar.gz",
    scripts      = ["gog-install"],
    classifiers  = [
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Development Status :: 5 - Production/Stable",
        "Environment :: Console",
        "Intended Audience :: End Users/Desktop",
        "License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)",
        "Operating System :: OS Independent",
        ],
)
