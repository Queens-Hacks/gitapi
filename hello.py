#!/usr/bin/env python

from test import SeededRepo, get_app

if __name__ == '__main__':
    with SeededRepo() as repo:
        api = get_app(repo.workdir)
        print('rules:')
        for rule in api.url_map.iter_rules():
            print('{:10s} {}'.format(', '.join(rule.methods), rule))
        api.run(debug=True)
