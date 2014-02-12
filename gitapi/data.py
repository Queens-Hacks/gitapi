# -*- coding: utf-8 -*-
"""
    gitapi.data
    ~~~~~~~~~~~

    Interface with git and stuff

    :license: BSD
"""

from werkzeug.routing import Rule


class GitData(object):
    """Use a folder of stuff as resource data"""

    def __init__(self, folder):
        self.folder = folder

    def register_urls(self, url_prefix, api):
        api.url_map.add(Rule(url_prefix + '/', methods=['GET'], endpoint=self.index))

    #         rules = (
    #     ('/', 'GET', index),
    #     ('/', 'POST', create),
    #     ('/<id>', 'GET', get),
    #     ('/<id>', 'PUT', update),
    #     ('/<id>', 'DELETE', remove),
    # )

    def index(self):
        return "yo yo yo!"

    def create(self, data):
        pass

    def get(self, id):
        pass

    def update(self, id, data):
        pass

    def delete(self, id):
        pass
