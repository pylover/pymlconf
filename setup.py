# -*- coding: utf-8 -*-
import os
try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

from pymlconf import __version__ as package_version


dependencies = ['pyyaml>=3.10']

try:
    from collections import OrderedDict
except:
    dependencies.append('ordereddict')


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name="pymlconf",
    version=package_version,
    author="Vahid Mardani",
    author_email="vahid.mardani@gmail.com",
    url="http://packages.python.org/pymlconf",
    description="Python high level configuration library",
    maintainer="Vahid Mardani",
    maintainer_email="vahid.mardani@gmail.com",
    packages=["pymlconf"],
    platforms=["any"],
    long_description=read('README.txt'),
    install_requires=dependencies,
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "License :: Freeware",
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Topic :: Software Development :: Libraries'
        ],
    )
