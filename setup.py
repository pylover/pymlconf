# -*- coding: utf-8 -*-
import os
import re
try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

# reading pymlconf version (same way sqlalchemy does)
v_file = open(os.path.join(os.path.dirname(__file__),
                        'pymlconf', '__init__.py'))
package_version = re.compile(r".*__version__ = '(.*?)'",
                     re.S).match(v_file.read()).group(1)
v_file.close()

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
    install_requires=['pyyaml>=3.10'],
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
