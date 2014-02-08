# -*- coding: utf-8 -*-
"""
    gitapi.api
    ~~~~~~~~~~

    The WSGI application yo.

    :license: BSD
"""

from werkzeug.datastructures import ImmutableDict
from werkzeug.routing import Map, Rule


class GitAPI(object):
    """This is it."""

    default_config = ImmutableDict({
        'DEBUG': False,
    })

    def __init__(self):
        self.config = dict(default_config)
        self.endpoint_map = Map()

    def run(self, host=None, port=None, debug=None, **options):
        """mostly copied from flask"""
        from werzeug.serving import run_simple
        host = host or '127.0.0.1'
        port = port or self.config.get('PORT') or 5000
        if debug is not None:
            self.debug = bool(debug)
        options.setdefault('use_reloader', self.debug)
        options.setdefault('use_debugger', self.debug)
        run_simple(host, port, self, **options)

    def add_resource_endpoint(self, url_root, resource):
        pass

    def wsgi_app(self, environ, start_response):
        pass

    def __call__(self, environ, start_response):
        pass

    def __repr__(self):
        return '<{}>'.format(self.__class__.__name__)
