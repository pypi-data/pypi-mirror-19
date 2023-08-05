#!/usr/bin/env python2.7

from setuptools import setup
import os

setup(
    name = "onetoonemap",
    version = "1.0.0",
    author = "Carl Seelye",
    author_email = "cseelye@gmail.com",
    description = "1:1 mapping collection type",
    license = "MIT",
    keywords = "1:1 map dict",
    packages = ["onetoonemap"],
    url = "https://github.com/cseelye/onetoonemap",
    long_description = open(os.path.join(os.path.dirname(__file__), "README.rst")).read(),
    install_requires = [
    ]
)

