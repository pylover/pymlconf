from os import path

import yaml

try:
    from yaml import CLoader as Loader
except ImportError:  # pragma: no cover
    from yaml import Loader


def preprocess(data, context):
    if callable(context):
        context = context()
    return data % context


def loads(str_data, context=None):
    if context:
        str_data = preprocess(str_data, context)
    return yaml.load(str_data, Loader)


def load(filename, context=None):
    directory = path.abspath(path.dirname(filename))
    context = context or {}
    context.update(here=directory)

    with open(filename) as f:
        return loads(f.read(), context)


def dumps(o):
    return yaml.dump(o, default_flow_style=False)
