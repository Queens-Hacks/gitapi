# -*- coding: utf-8 -*-
"""
    gitapi.resource
    ~~~~~~~~~~~~~~~

    Models of the data, sorta

    :license: BSD
"""


def list(resource_class, only_current=True):
    """List available resources"""
    # walk the tree for ids


def create(resource_class, data):
    """create a new resource"""
    # try to instantiate a resource
    # check if the id collides


def get(resource_class, resource_id):
    """get an individual resource"""


def update(resource_class, resource_id, data):
    """modify an existing resource"""


def delete(resource_class, resource_id):
    """remove a resource"""


class Resource(object):
    """Basic representations of data.

    Resources map directly to files on disk (or tracked in git).
    """

    def __init__(self):
        pass

    def __repr__(self):
        return '<{}: {}>'.format(self.__class__.__name__, id(self))
