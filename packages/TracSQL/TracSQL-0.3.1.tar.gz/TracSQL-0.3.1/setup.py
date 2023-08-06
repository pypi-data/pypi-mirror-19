#!/usr/bin/env python

import os.path
from distutils.core import setup

# Utility function to read the README file.
def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name = 'TracSQL',
    version = '0.3.1',
    description = "A Trac plugin for querying the project database",
    long_description = read('README.md'),
    author = "John Benediktsson",
    author_email = 'mrjbq7@gmail.com',
    url = "http://github.com/trac-hacks/tracsql",
    download_url = "http://github.com/trac-hacks/tracsql/zipball/master#egg=TracSQL-0.3",
    packages = ['tracsql'],
    package_data={
        'tracsql': [
            'htdocs/*.css',
            'htdocs/*.png',
            'htdocs/*.gif',
            'htdocs/*.js',
            'templates/*.html'
        ]
    },
    entry_points = {
        'trac.plugins': [
            'tracsql.web_ui = tracsql.web_ui',
        ]
    },
    dependency_links = ['http://github.com/trac-hacks/tracsql/zipball/master#egg=TracSQL-0.3']
)

