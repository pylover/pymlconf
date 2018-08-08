# -*- coding: utf-8 -*-
import os
import sys
import re

from setuptools import setup, find_packages

# reading pymlconf version (same way sqlalchemy does)
with open(
    os.path.join(os.path.dirname(__file__), 'pymlconf', '__init__.py')
) as v_file:
    package_version = \
        re.compile(r".*__version__ = '(.*?)'", re.S) \
        .match(v_file.read()) \
        .group(1)


dependencies = ['pyyaml >= 3.10']


def read(filename):
    return open(os.path.join(os.path.dirname(__file__), filename)).read()

setup(
    name="pymlconf",
    version=package_version,
    author="Vahid Mardani",
    author_email="vahid.mardani@gmail.com",
    url="http://github.com/pylover/pymlconf",
    description="Another configuration library using yaml",
    packages=find_packages(),
    package_data={'pymlconf': ['tests/conf/*', 'tests/files/*']},
    platforms=["any"],
    long_description=read('README.rst'),
    install_requires=dependencies,
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "License :: OSI Approved :: MIT License",
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3.6',
        'Topic :: Software Development :: Libraries'
    ],
    test_suite='pymlconf.tests',
)
