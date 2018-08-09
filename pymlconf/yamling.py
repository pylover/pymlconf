from os import path

from yaml import load

try:
    from yaml import CLoader as Loader
except ImportError:  # pragma: no cover
    from yaml import Loader


def pre_process(data, context):
    if callable(context):
        context = context()
    return data % context


def load_string(str_data, context=None):
    if context:
        str_data = pre_process(str_data, context)
    return load(str_data, Loader)


def load_yaml(filename, context=None):
    directory = path.abspath(path.dirname(filename))
    context = context or {}
    context.update(here=directory)

    with open(filename) as f:
        return load_string(f.read(), context)

