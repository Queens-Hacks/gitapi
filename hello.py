#!/usr/bin/env python

from gitapi import GitAPI, Resource

api = GitAPI('gitapidatatest')


class Student(Resource):
    folder = 'students'
    url_prefix = '/students'
    files = True


api.add_resource_endpoint(Student)


if __name__ == '__main__':
    print('rules:')
    for rule in api.url_map.iter_rules():
        print(rule)
    api.run(debug=True)
