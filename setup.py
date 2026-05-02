import os
import re

from setuptools import setup


# reading pymlconf version (same way sqlalchemy does)
with open(
    os.path.join(os.path.dirname(__file__), 'pymlconf.py')
) as v_file:
    package_version = \
        re.compile(r".*__version__ = '(.*?)'", re.S) \
        .match(v_file.read()) \
        .group(1)


dependencies = [
    'pyyaml >= 6.0.3'
]


setup(
    name="pymlconf",
    version=package_version,
    author="Vahid Mardani",
    author_email="vahid.mardani@gmail.com",
    url="http://github.com/pylover/pymlconf",
    description="Another configuration library using yaml",
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',  # This is important!
    py_modules=['pymlconf'],
    platforms=["any"],
    install_requires=dependencies,
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12',
        'Topic :: Software Development :: Libraries'
    ],
)
