"""pymlconf package."""
__version__ = '4.0.0'


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


def include(loader, node):
    with open(node.value) as f:
        return load(f)


def env(loader, node):
    return os.environ.get(node.value)


def shell(loader, node):
    result = subprocess.run(
        node.value,
        shell=True,
        check=True,
        text=True,
        capture_output=True,
    )

    return result.stdout.strip()


Loader.add_constructor('!include', include)
Loader.add_constructor('!env', env)
Loader.add_constructor('!shell', shell)


class Meld(dict):
    def __init__(self, data=None, file=None):
        super().__init__()
        if data is not None:
            self |= data

        if file:
            self.load(file)

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
            if isinstance(mine, Meld):
                mine |= other
            elif isinstance(other, dict):
                self[k] = Meld(other)
            else:
                self[k] = other

        return self

    def __getattr__(self, key):
        if key not in self:
            raise AttributeError(key)

        return self[key]

    def __setattr__(self, key, value):
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
