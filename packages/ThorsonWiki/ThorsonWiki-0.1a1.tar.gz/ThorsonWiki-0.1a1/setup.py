#!/usr/bin/env python

import os

from setuptools import find_packages, setup

DESCRIPTION = "Fast and modular wiki sites with Django"

def readfile(filename):
    """
    Reads a file from the same directory as this one.
    """

    with open(os.path.join(os.path.dirname(__file__), filename)) as infile:
        return infile.read()

setup(
    name='ThorsonWiki',
    version='0.1a1',
    author="Jacob Collard",
    author_email="jacob@thorsonlinguistics.com",
    description=DESCRIPTION,
    license="MIT",
    url="https://github.com/thorsonlinguistics/thorson_wiki",
    packages=find_packages(),
    long_description=readfile('description.rst'),
    install_requires=['bleach', 'django', 'django-widget-tweaks', 'markdown'],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Environment :: Web Environment",
        "Framework :: Django :: 1.10",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 3",
    ]
)
