
import os.path
from yaml import load
from yaml.scanner import ScannerError
from pymlconf.errors import ConfigFileSyntaxError
try:
    from yaml import CLoader as Loader
except ImportError:
    from yaml import Loader


# def _normalize(content):
#     return content.replace('\t', ' ')


def pre_process(data, macros):
    if callable(macros):
        macros = macros()
    return data % macros


def load_string(str_data, macros=None):
    if macros:
        str_data = pre_process(str_data, macros)
    return load(str_data, Loader)


def load_yaml(file_path, macros=None, encoding='utf-8'):
    stream = open(file_path, encoding=encoding)
    file_dir = os.path.abspath(os.path.dirname(file_path))
    macros = {} if macros is None else macros
    macros.update(here=file_dir)
    try:
        return load_string(stream.read(), macros)
    except ScannerError as ex:
        raise ConfigFileSyntaxError(file_path, ex)
    finally:
        stream.close()
