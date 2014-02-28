# -*- coding: utf-8 -*-
"""
    gitapi.data
    ~~~~~~~~~~~

    Interface with git and stuff

    :license: BSD
"""

import os
import yaml
from werkzeug.routing import Rule
from werkzeug.security import safe_join
from werkzeug.exceptions import NotFound, BadRequest


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

    def index(self, request):
        entries = (e for e in self.repo.index
                   if e.path.startswith(self.resource.folder + '/'))
        lalala = ((e.path, self.repo.get(e.hex).data) for e in entries)
        return [self.resource(path, yaml.load(data)) for path, data in lalala]

    def create(self, request):
        # print('\n'.join(dir(request)))
        try:
            # this mapping should be generated from the Resource schema
            noob = {'name': str(request.form['name']),
                    'last': str(request.form['last']),
                    'who': str(request.form['who'])}
        except KeyError:
            raise BadRequest
        serialized = yaml.dump(noob)
        blob = self.repo.create_blob(serialized)
        

        return "Y"

    def get(self, request, resource_id):
        path = safe_join(self.resource.folder, resource_id)
        if path is None:
            raise NotFound()
        if self.resource.files:
            path += '.yaml'
        try:
            entry = self.repo.index[path]
        except KeyError:
            raise NotFound()
        raw_data = self.repo.get(entry.hex).data
        data = yaml.load(raw_data)
        resource = self.resource(path, data)
        return resource

    def update(self, request, resource_id):
        return "replace with something\n"

    def patch(self, request, resource_id):
        return "update something specific\n"

    def delete(self, request, resource_id):
        return "remove that.\n"
