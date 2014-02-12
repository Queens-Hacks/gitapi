#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
    setup
    ~~~~~

    Install this stuff blah blah blah
"""

from setuptools import setup


setup(
    name="GitAPI",
    version="0.0.1",
    description="A",
    long_description=open('README.rst').read(),
    license='BSD',
    url='http://github.com/Queens-Hacks/gitapi',
    install_requires=[
        "PyYaml",
        "pyrx",
        "Werkzeug",
        "venvgit2"
    ],
)
