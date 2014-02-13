# -*- coding: utf-8 -*-
"""
    gitapi.data
    ~~~~~~~~~~~

    Interface with git and stuff

    :license: BSD
"""

import os
from werkzeug.routing import Rule
from werkzeug.exceptions import NotFound


class GitData(object):
    """Use a folder of stuff as resource data"""

    def __init__(self, resource, repo):
        self.resource = resource
        self.repo = repo

    def register_urls(self, url_prefix, api):
        route = lambda method, rule, endpoint: api.url_map.add(
                Rule(url_prefix + rule, methods=[method], endpoint=endpoint))

        route('GET',   '/', self.index)
        route('POST',  '/', self.create)
        route('GET',   '/<resource_id>', self.get)
        route('PUT',   '/<resource_id>', self.update)
        route('PATCH', '/<resource_id>', self.patch)
        route('DELETE','/<resource_id>', self.delete)

    def index(self):
        return "yo yo yo!\n"

    def create(self):
        return "should create some stuff\n"

    def get(self, resource_id):
        #### WARNING -- use a safe_join... does werkzeug have one?
        path = os.path.join(self.resource.folder, resource_id)
        print('using path', path)
        try:
            entry = self.repo.index[path]
        except KeyError:
            raise NotFound()
        data = self.repo.get(entry.hex).data
        return data + "\n"

    def update(self, resource_id):
        return "replace with something\n"

    def patch(self, resource_id):
        return "update something specific\n"

    def delete(self, resource_id):
        return "remove that.\n"
