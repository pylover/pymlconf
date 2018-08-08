import sys
from collections import Iterable, OrderedDict
from StringIO import StringIO


def isiterable(o):
    if isinstance(o, (bytes, str, type)):
        return False
    return isinstance(o, Iterable)

