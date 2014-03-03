"""
    test
    ~~~~

    Utilities for testing gitapi.

    :licence: MIT
"""

import os
import shutil
import tempfile
import unittest
import pygit2
from gitapi import GitAPI


course_schema = """type: //rec
required:
  name: //str
  description: //str
optional:
  instructor:
    type: //ref
    folder: instructors
"""

instructor_schema = """type: //rec
required:
  name: //str
"""


def get_app(repo):
    app = GitAPI(repo)
    courses = app.data_resource('courses', '/courses', schema=course_schema)
    @courses.id_generator
    def generate_course_id(course_data):
        return "abc123"
    instructors = app.data_resource('instructors', '/instructors', schema=instructor_schema)
    @instructors.id_generator
    def generate_instructor_id(instructor_data):
        return instructor_data['name'].lower().replace(' ', '-')
    return app


def seed(repo):
    """Create a testable data repo

    The file layout is like this:

        /
          /courses
            cisc-121.yml
            cisc-124.yml
          /instructors
            alan-mcleod.yml
            margaret-lamb.yml

    """
    tree = repo.TreeBuilder()

    courses_tree = repo.TreeBuilder()
    def insert_course(id, name, desc, instructor):
        template ='name: {}\ndescription: {}\ninstructor: \n' \
                  '  ref: instructors/{}\n'
        blob = repo.create_blob(template.format(name, desc, instructor))
        courses_tree.insert(id + '.yml', blob, pygit2.GIT_FILEMODE_BLOB)
    insert_course('cisc-121', 'Introduction to Computing Science I',
                  'Introduction to design and analysis of algorithms.',
                  'margaret-lamb')
    insert_course('cisc-124', 'Introduction to Computing Science II',
                  'Introduction to object-oriented design, architecture...',
                  'alan-mcleod')
    tree.insert('courses', courses_tree.write(), pygit2.GIT_FILEMODE_TREE)

    instructors_tree = repo.TreeBuilder()
    def insert_instructor(id, name):
        blob = repo.create_blob('name: {}\n'.format(name))
        instructors_tree.insert(id + '.yml', blob, pygit2.GIT_FILEMODE_BLOB)
    insert_instructor('margaret-lamb', 'Margaret Lamb')
    insert_instructor('alan-mcleod', 'Alan McLeod')
    tree.insert('instructors', instructors_tree.write(), pygit2.GIT_FILEMODE_TREE)

    tree_oid = tree.write()

    committer = author = pygit2.Signature('Tester', 'tester@example.com')
    init_commit_oid = repo.create_commit(
        'refs/heads/master', author, committer,
        'Seed commit\n\nSet up some seed data for testing.',
        tree_oid, []
    )
    repo.checkout('refs/heads/master')
    


class EmptyRepo(object):
    """An empty repository in a temporary directory that will be cleaned up."""

    def __enter__(self):
        """Create an empty repository to play with."""
        self.repo_dir = tempfile.mkdtemp()
        repo = pygit2.init_repository(self.repo_dir)
        return repo

    def __exit__(self, *exc_args):
        """Clean up the empty repo."""
        shutil.rmtree(self.repo_dir)


class SeededRepo(EmptyRepo):
    """Like `EmptyRepo`, but with sample data for testing."""
    def __enter__(self):
        repo = super(SeededRepo, self).__enter__()
        seed(repo)
        return repo


def test_nothing():
    with SeededRepo() as repo:
        app = get_app(repo.workdir)
