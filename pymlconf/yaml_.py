import functools

import yaml
try:
    from yaml import CLoader as Loader
except ImportError:  # pragma: no cover
    from yaml import Loader


load = functools.partial(yaml.load, Loader)
dump = functools.partial(yaml.dump, default_flow_style=False)


def loadfile(filename):
    with open(filename) as f:
        return load(f.read())
