import functools

import yaml
try:
    from yaml import CLoader as Loader
except ImportError:  # pragma: no cover
    from yaml import Loader


load = functools.partial(yaml.load, Loader=Loader)
dump = functools.partial(yaml.dump, default_flow_style=False)


def loadfile(file):
    if isinstance(file, str):
        with open(file) as f:
            return loadfile(f)

    return load(file)
