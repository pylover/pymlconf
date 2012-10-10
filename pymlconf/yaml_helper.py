

from yaml import load
try:
    from yaml import CLoader as Loader
except ImportError:
    from yaml import Loader

def _normalize(content):
    return content.replace('\t', ' ')

def load_yaml(filepath):
    stream = open(filepath)
    try:
        return load(_normalize(stream.read()), Loader)
    finally:
        stream.close()

def load_string(str_data):
    return load(_normalize(str_data), Loader)
