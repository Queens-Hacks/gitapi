# -*- coding: utf-8 -*-
"""
    gitapi.resource
    ~~~~~~~~~~~~~~~

    Models of the data, sorta

    :license: BSD
"""


class Resource(object):
    """Basic representations of data.

    Resources map directly to files on disk (or tracked in git).
    """

    def __repr__(self):
        return '<{}: {}>'.format(self.__class__.__name__, id(self))
