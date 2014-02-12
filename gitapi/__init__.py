# -*- coding: utf-8 -*-
"""
    gitapi
    ~~~~~~

    A git-backed API microframework built on Werkzeug. Inspired by Flask.

    :license: BSD
"""

# Expose things to the public interface
from api import GitAPI
from resource import Resource
from schema import Reference, Indexed, Record
from data import GitData
