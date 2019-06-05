from os import path

import yaml

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
    return yaml.load(str_data, Loader)


def load_file(filename, context=None):
    directory = path.abspath(path.dirname(filename))
    context = context or {}
    context.update(here=directory)

    with open(filename) as f:
        return load_string(f.read(), context)


def  dump_yaml(o):
    return yaml.safe_dump(o)
