# -*- coding: utf-8 -*-
"""
    gitapi.api
    ~~~~~~~~~~

    The WSGI application yo.

    :license: BSD
"""

from pygit2 import Repository
from werkzeug.routing import Map, Rule
from werkzeug.wrappers import Request, Response
from werkzeug.datastructures import ImmutableDict
from data import GitData


class GitAPI(object):
    """The WSGI app exposing your API"""

    default_config = ImmutableDict({
        'DEBUG': False,
        'DATA_LOCAL': None,
        'DATA_REMOTE': None,
    })

    def __init__(self, git_dir):
        self.config = dict(self.default_config)
        self.resources = {}
        self.endpoint_funcs = {}
        self.url_map = Map()
        self.repo = Repository(git_dir)

    def run(self, host=None, port=None, debug=None, **options):
        """mostly copied from flask"""
        from werkzeug.serving import run_simple
        host = host or '127.0.0.1'
        port = port or self.config.get('PORT') or 5000
        self.debug = bool(debug) if debug is not None else self.config['DEBUG']
        options.setdefault('use_reloader', self.debug)
        options.setdefault('use_debugger', self.debug)
        run_simple(host, port, self, **options)

    def add_resource_endpoint(self, url_prefix, resource):
        assert resource.folder not in self.resources, \
            "{}: Resources can only be registered once".format(resource.folder)
        self.resources[resource.folder] = resource
        resource.data = GitData(resource, self.repo)
        resource.data.register_urls(url_prefix, self)

    def wsgi_app(self, environ, start_response):
        """Blah blah blah"""
        request = Request(environ)
        urls = self.url_map.bind_to_environ(environ)
        endpoint, args = urls.match()
        resp = endpoint(**args)
        response = Response(resp)
        return response(environ, start_response)

    def __call__(self, environ, start_response):
        """Shortcut for :attr:`wsgi_app`."""
        return self.wsgi_app(environ, start_response)

    def __repr__(self):
        return '<{}: {}>'.format(self.__class__.__name__, id(self))
