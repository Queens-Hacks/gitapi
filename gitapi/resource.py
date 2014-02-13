# -*- coding: utf-8 -*-
"""
    gitapi.resource
    ~~~~~~~~~~~~~~~

    Models of the data, sorta

    :license: BSD
"""


class Resource(dict):
    """Basic representations of data.

    Resources map directly to files on disk (or tracked in git).
    """

    def __init__(self, path, *args, **kwargs):
        print(args)
        super(Resource, self).__init__(*args, **kwargs)
        extless = path[:-len('.yaml')] if self.files else path
        my_id = extless.split('/', 1)[1]
        self.update(link=self.url_prefix + '/' + my_id)

    def __repr__(self):
        return '<{}: {}>'.format(self.__class__.__name__, id(self))
