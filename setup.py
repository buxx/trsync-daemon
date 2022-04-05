#!/usr/bin/env python

from distutils.core import setup

setup(
    name="Trsync Desktop",
    version="1.0",
    description="Desktop application of trsync",
    author="Bastien Sevajol",
    author_email="bastien@sevajol.fr",
    url="https://github.com/buxx/trsync",
    packages=["trsync_desktop"],
    entry_points={"console_scripts": ["trsync-desktop=trsync_desktop.run:run"]},
)
