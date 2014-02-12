# -*- coding: utf-8 -*-
"""
    gitapi.schema
    ~~~~~~~~~~~~~

    Wrap rx types in python classes, making the code a bit more readable with
    better errors and nifty stuff like Indexed.

    :license: BSD
"""


class TypeBase(object):
    """la la la"""

    def __new__(cls, typ):
        return super(TypeBase, cls).__new__(cls, typ)

    def __str__(self):
        return self.rx


class Indexed(TypeBase):
    """Buid a hash map of values for keys to resources"""

    @property
    def rx(self):
        return self.rx_type.rx

    def __init__(rx_type, unique=True):
        self.rx_type = rx_type
        self.unique = unique


class Reference(TypeBase):
    """Refer to another resource"""

    rx = '//str'

    def __init__(folder):
        self.folder = folder


class Record(TypeBase):
    """Wrap rx's record type"""

    rx = '//rec'


