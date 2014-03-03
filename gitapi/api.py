# -*- coding: utf-8 -*-
"""
    gitapi.api
    ~~~~~~~~~~

    The WSGI application yo.

    :license: BSD
"""

import os
import json
import yaml
import pygit2
from pyrx import RxError, Factory as SchemaFactory, _CoreType as PyrxType
from werkzeug.routing import Map, Rule
from werkzeug.wrappers import Request, Response
from werkzeug.exceptions import BadRequest
from werkzeug.datastructures import ImmutableDict


class GitAPI(object):
    """The WSGI app exposing your API"""

    default_config = ImmutableDict({
        'DEBUG': False,
        'DATA_LOCAL': None,
        'DATA_REMOTE': None,
    })

    def __init__(self, git_dir):
        self.config = dict(self.default_config)
        self.repo = pygit2.Repository(git_dir)
        self.resources = {}
        self.endpoint_funcs = {}
        self.url_map = Map()

    def data_resource(self, folder, url_prefix, schema):
        assert folder not in self.resources, \
            "{}: Resource names gotta be unique yo.".format(resource.folder)
        resource = Resource(folder, schema)
        self.resources[folder] = resource
        resource.register(self, url_prefix, self.repo)
        return resource

    def run(self, host=None, port=None, debug=None, **options):
        """Run a development server. Mostly copied from flask."""
        from werkzeug.serving import run_simple
        host = host or '127.0.0.1'
        port = port or self.config.get('PORT') or 5000
        self.debug = bool(debug) if debug is not None else self.config['DEBUG']
        options.setdefault('use_reloader', self.debug)
        options.setdefault('use_debugger', self.debug)
        run_simple(host, port, self, **options)

    def wsgi_app(self, environ, start_response):
        """Serve WSGI requests"""
        request = Request(environ)
        urls = self.url_map.bind_to_environ(environ)
        endpoint, args = urls.match()
        resp_data = endpoint(request, **args)
        json_string = json.dumps(resp_data, indent=2)
        response = Response(json_string)
        return response(environ, start_response)

    def __call__(self, environ, start_response):
        """Shortcut for :attr:`wsgi_app`."""
        return self.wsgi_app(environ, start_response)

    def __repr__(self):
        return '<{}: {}>'.format(self.__class__.__name__, id(self))


class RefType(PyrxType):
    """A custom rx type for references to other resources"""

    @staticmethod
    def subname():
        return 'ref'

    def __init__(self, schema, rx):
        """Make sure the schema is legal"""
        if not set(schema.keys()) <= set(('type', 'folder')):
            raise RxError('unknown parameter for //ref')
        try:
            self.folder = schema['folder']
        except KeyError:
            raise RxError('type //ref needs a folder')

    def check(self, value):
        parts = value.split('/')
        if len(parts) != 2:
            return False
        folder, data_id = parts
        if not folder == self.folder:
            return False
        return True


class Resource(object):

    def __init__(self, folder, schema):
        self.folder = folder
        rx = SchemaFactory({'register_core_types': True})
        rx.register_type(RefType)
        schema_data = yaml.load(schema)
        self.schema = rx.make_schema(schema_data)
        self._id_generator = None

    def register(self, api, url_prefix, repo):
        self.api = api
        self.url_prefix = url_prefix
        self.repo = repo

        # Register URL rules
        route = lambda method, rule, endpoint: api.url_map.add(
                Rule(url_prefix + rule, methods=[method], endpoint=endpoint))
        route('GET',   '/', self.index)
        route('POST',  '/', self.create)
        route('GET',   '/<resource_id>', self.get)
        route('PUT',   '/<resource_id>', self.update)
        route('PATCH', '/<resource_id>', self.patch)
        route('DELETE','/<resource_id>', self.delete)

    def id_generator(self, func):
        self._id_generator = func
        return func

    def get_tree(self):
        resource_treeentry = self.repo.head.get_object().tree[self.folder]
        folder_tree = self.repo.get(resource_treeentry.oid)
        return folder_tree

    def ref_to_resource(self, data_id, hex_sha1):
        # 0. Convert id (strip suffix)
        resource_id = os.path.splitext(data_id)[0]
        # 1. Load data
        raw_data = self.repo.get(hex_sha1).data
        data = yaml.load(raw_data)
        print(data)
        # 2. Convert refs to links
        def refs_to_links(data):
            for key, val in data.items():
                if isinstance(val, dict):
                    data[key] = refs_to_links(val)
                if 'ref' in val:
                    link = self.ref_to_link(val['ref'])
                    data[key] = link
                    
        refs_to_links(data)
        # 3. Inject a link to self
        self_data_ref = '/'.join((self.folder, data_id))
        data.update(self.ref_to_link(self_data_ref))
        return data

    def ref_to_link(self, ref):
        folder, data_id = ref.split('/')
        resource_id = os.path.splitext(data_id)[0]
        link_url_prefix = self.api.resources[folder].url_prefix
        link = '/'.join((link_url_prefix, resource_id))
        return {'link': link}

    def get_test_treebuilders(self):
        if 'test' not in self.repo.listall_branches():
            self.repo.create_branch('test', self.repo.head.get_object())
        tree = self.repo.lookup_branch('test').get_object().tree
        treebuilder = self.repo.TreeBuilder(tree)
        resource_subtree_entry = tree[self.folder]
        resource_subtree = self.repo.get(resource_subtree_entry.oid)
        resource_treebuilder = self.repo.TreeBuilder(resource_subtree)
        return treebuilder, resource_treebuilder

    def index(self, request):
        """List all instances of this resource.
        Iterates through the folder and grab data for every entry.
        """
        raw_data = ((e.name, e.hex) for e in self.get_tree())
        return [self.ref_to_resource(id_, sha1) for id_, sha1 in raw_data]

    def create(self, request):
        # 1. Convert and validate data
        raw_data = request.get_data()
        data = json.loads(raw_data)
        if not self.schema.check(data):
            raise BadRequest()
        # 2. Generate an ID
        id_ =  self._id_generator(data)
        data_id = id_ + '.yml'
        # 3. Write the new data to a branch
        if 'test' not in self.repo.listall_branches():
            self.repo.create_branch('test', self.repo.head.get_object())
        blob_oid = self.repo.create_blob(yaml.dump(data))
        treebuilder, subtreebuilder = self.get_test_treebuilders()
        subtreebuilder.insert(data_id, blob_oid, pygit2.GIT_FILEMODE_BLOB)
        subtree_oid = subtreebuilder.write()
        treebuilder.insert(self.folder, subtree_oid, pygit2.GIT_FILEMODE_TREE)
        tree_oid = treebuilder.write()
        committer = author = pygit2.Signature('API Person', 'api@example.com')
        commit_oid = self.repo.create_commit(
            'refs/heads/test', author, committer,
            'Some update....',
            tree_oid, [self.repo.lookup_branch('test').get_object().oid],
        )
        return 'make a new one'

    def get(self, request, resource_id):
        data_id = resource_id + '.yml'
        entry = self.get_tree()[data_id]
        return self.ref_to_resource(entry.name, entry.hex)

    def update(self, request, resource_id):
        return 'update this one {}'.format(resource_id)

    def patch(self, request, resource_id):
        return 'patch this one {}'.format(resource_id)

    def delete(self, request, resource_id):
        return 'delete this one {}'.format(resource_id)
