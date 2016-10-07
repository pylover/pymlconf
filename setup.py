# -*- coding: utf-8 -*-
import os
import sys
import re
try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

# reading pymlconf version (same way sqlalchemy does)
with open(os.path.join(os.path.dirname(__file__), 'pymlconf', '__init__.py')) as v_file:
    package_version = re.compile(r".*__version__ = '(.*?)'", re.S).match(v_file.read()).group(1)

dependencies = ['pyyaml >= 3.10']

# checking for current python version to add legacy `ordereddict` module into dependencies
if sys.version_info < (2, 7):
    dependencies.append('ordereddict')


def read(filename):
    return open(os.path.join(os.path.dirname(__file__), filename)).read()

setup(
    name="pymlconf",
    version=package_version,
    author="Vahid Mardani",
    author_email="vahid.mardani@gmail.com",
    url="http://github.com/pylover/pymlconf",
    description="Python high level configuration library",
    maintainer="Vahid Mardani",
    maintainer_email="vahid.mardani@gmail.com",
    packages=["pymlconf", "pymlconf.tests"],
    package_dir={'pymlconf': 'pymlconf'},
    package_data={'pymlconf': ['tests/conf/*', 'tests/files/*']},
    platforms=["any"],
    long_description=read('README.rst'),
    install_requires=dependencies,
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "License :: Freeware",
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Topic :: Software Development :: Libraries'
    ],
    test_suite='pymlconf.tests',
)
