import sys

import yaml
from yaml import YAMLError

try:
    from yaml import CLoader as Loader
except ImportError:  # pragma: no cover
    from yaml import Loader


def loads(string):
    try:
        return yaml.load(string, Loader)

    except YAMLError as ex:
        print('YAML parsing error', file=sys.stderr)
        print('Input string start', file=sys.stderr)
        print(string, file=sys.stderr)
        print('Input string end', file=sys.stderr)
        raise ex


def load(filename):
    with open(filename) as f:
        return loads(f.read())


def dumps(o):
    return yaml.dump(o, default_flow_style=False)
