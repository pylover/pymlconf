
from pymlconf.mergable import Mergable
from pymlconf.errors import ConfigKeyError
from pymlconf.compat import OrderedDict, isiterable
import copy


def _make_mergable_if_possible(data):
    if isinstance(data, dict):
        return ConfigDict(data=data)
    elif isiterable(data):
        return ConfigList([_make_mergable_if_possible(i) for i in data])
    else:
        return data


class ConfigDict(OrderedDict, Mergable):

    def __init__(self, data=None):
        OrderedDict.__init__(self)
        Mergable.__init__(self, data=data)

    def can_merge(self, data):
        return data and isinstance(data, dict)

    def _merge(self, data):
        for k in list(data.keys()):
            v = data[k]

            if k in self \
                and isinstance(self[k], Mergable) \
                and self[k].can_merge(v):
                self[k].merge(v)
            else:
                if isinstance(v, Mergable):
                    self[k] = v.copy()
                else:
                    self[k] = _make_mergable_if_possible(copy.deepcopy(v))

    def __getattr__(self, key):
        if key in self:
            return self.get(key)
        raise ConfigKeyError(key)

    def __setattr__(self, key, value):
        if not key in self:
            self.__dict__[key] = value
        else:
            self[key] = value

    def _ensure_namespaces(self, *namespaces):
        if namespaces:
            ns = namespaces[0]
            if ns not in self:
                self[ns] = ConfigDict()
            return self.__getattr__(ns)._ensure_namespaces(*namespaces[1:])
        else:
            return self

    def copy(self):
        return self.__class__(self)

    @classmethod
    def empty(cls):
        return cls()


class ConfigList(list, Mergable):

    def __init__(self, data=None):
        list.__init__(self)
        Mergable.__init__(self, data=data)

    def can_merge(self, data):
        return data and hasattr(data, '__iter__')

    def merge(self, data):
        for item in data:
            if item not in self:
                self.append(item)

    @classmethod
    def empty(cls):
        return cls()
