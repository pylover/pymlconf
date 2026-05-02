#!/usr/bin/env python3

import os
import re
import sys


sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

html_theme = 'python_docs_theme'

extensions = [
    'sphinx.ext.doctest',
    'sphinx.ext.autodoc',
    'sphinx.ext.intersphinx',
]

# Add any paths that contain templates here, relative to this directory.
templates_path = ['_templates']

# General information about the project.
project = 'pymlconf'
copyright = '2016, Vahid Mardani'
author = 'Vahid Mardani'


# reading package's version (same way sqlalchemy does)
with open(
    os.path.join(os.path.dirname(__file__), '../pymlconf.py')
) as v_file:

    package_version = \
        re.compile('.*__version__ = \'(.*?)\'', re.S)\
        .match(v_file.read())\
        .group(1)


version = '.'.join(package_version.split('.')[:2])
release = package_version

exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']
html_static_path = ['_static']
autodoc_default_flags = [
    'members',
    'show-inheritance',
]

intersphinx_mapping = {
    'python': ('https://docs.python.org/3.12', None),
}

html_title = 'pymlconf Documentation'
html_show_sourcelink = False
