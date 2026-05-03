"""pymlconf package."""
__version__ = '4.1.1'


import os
import copy
import functools
import subprocess

import yaml
try:
    from yaml import CLoader as Loader
except ImportError:  # pragma: no cover
    from yaml import Loader


load = functools.partial(yaml.load, Loader=Loader)
MAPPING_TAG = 'tag:yaml.org,2002:map'


class Meld(dict):
    """Replacement for default yaml mapping.

    This class has the ability to merge with other mappings such as
    py:class:`dict` and it's subclasses. so any configuration node can be
    merged with other.

    :param data: ``yaml string``, list of 2-tuples or dict.
    :param file: file object or filename to load.
    :param root: enclose the ``data`` argument in another key specified by
                 this argument.

    .. versionadded:: 4.1
       ``root`` parameter.

    The API is so simple:

    Create configuration instance with default value and load a file to
    overwrite:

    .. code-block::

       m = Meld('''
         foo:
           bar: BAR
           baz: BAZ
       ''', file='qux.yml')

    Merge/meld other mappings in:

    .. code-block::

       m |= dict(thud='THUD', corge=10)


    Load a file by name:

    .. code-block::

       m.load('foo.yml')

    Load a file-like object :

    .. code-block::

       with open('foo.yml') as f:
           m.load(f)

    Dump a Meld object:

    .. code-block::

       print(m.dump())
    """

    def __init__(self, data=None, file=None, root=None):
        super().__init__()
        if root:
            self[root] = Meld()
            root = self[root]
        else:
            root = self

        if data is not None:
            if not isinstance(data, str):
                data = dict(data)

            root |= data

        if file:
            root.load(file)

    def __ior__(self, data):
        if isinstance(data, str):
            data = load(data)
            docopy = False
        else:
            docopy = True

        if not isinstance(data, dict):
            raise TypeError(
                'Only dict and or it\'s subclasses are allowed, '
                f'given: {type(data)}')

        if docopy:
            data = copy.deepcopy(data)

        for k in data:
            mine = self.get(k)
            other = data.get(k)

            if not isinstance(other, Meld) and isinstance(other, dict):
                other = Meld(other)

            if isinstance(mine, Meld):
                mine |= other
            else:
                self[k] = other

        return self

    def __getattr__(self, key):
        if key not in self:
            raise AttributeError(key)

        return self[key]

    def __setattr__(self, key, value):
        if isinstance(value, dict):
            super().__setitem__(key, Meld(value))
            return

        super().__setitem__(key, value)

    def __delattr__(self, key):
        if key not in self:
            raise AttributeError(key)

        del self[key]

    def load(self, file):
        if isinstance(file, str):
            with open(file) as f:
                self.load(f)
                return

        self |= load(file)

    def dump(self, **kw):
        return yaml.dump(self, **kw)


def meld_representer(dumper, data):
    return dumper.represent_mapping(MAPPING_TAG, data)


def include_constructor(loader, node):
    with open(node.value) as f:
        return load(f)


def env_constructor(loader, node):
    return os.environ.get(node.value)


def shell_constructor(loader, node):
    result = subprocess.run(
        node.value,
        shell=True,
        check=True,
        text=True,
        capture_output=True,
    )

    return result.stdout.strip()


yaml.add_representer(Meld, meld_representer)
Loader.add_constructor('!include', include_constructor)
Loader.add_constructor('!env', env_constructor)
Loader.add_constructor('!shell', shell_constructor)
