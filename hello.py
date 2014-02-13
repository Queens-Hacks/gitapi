#!/usr/bin/env python

from gitapi import GitAPI, Resource

api = GitAPI('gitapidatatest')


class Student(Resource):
    
    folder = 'students'


api.add_resource_endpoint('/students', Student)


if __name__ == '__main__':
    print('rules:')
    for rule in api.url_map.iter_rules():
        print(rule)
    api.run(debug=True)
