# coding: utf-8

import sys
from setuptools import setup, find_packages

NAME = "pollster"
VERSION = "2.0.0"

# To install the library, run the following
#
# python setup.py install
#
# prerequisite: setuptools
# http://pypi.python.org/pypi/setuptools

REQUIRES = ["urllib3 >= 1.15", "six >= 1.10", "certifi", "python-dateutil", "pandas >= 0.19.1"]

setup(
    name=NAME,
    version=VERSION,
    description="Pollster API",
    author_email="Adam Hooper <adam.hooper@huffingtonpost.com>",
    url="https://github.com/huffpostdata/python-pollster",
    keywords=["Pollster API"],
    install_requires=REQUIRES,
    packages=find_packages(),
    include_package_data=True,
    long_description="""Download election-related polling data from Pollster."""
)

