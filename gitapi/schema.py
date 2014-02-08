# -*- coding: utf-8 -*-
"""
    gitapi.schema
    ~~~~~~~~~~~~~

    Magic

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
        return self.type_.rx

    def __init__(type_):
        self.type_ = type_


class Reference(TypeBase):
    """Refer to another resource"""

    rx = '//str'

    def __init__(folder):
        self.folder = folder


class Record(TypeBase):
    """Wrap rx's record type"""

    rx = '//rec'


