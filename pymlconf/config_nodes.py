
import abc
from pymlconf.errors import ConfigKeyError, ConfigurationMergeError
from pymlconf.compat import OrderedDict, isiterable
from pymlconf.yaml_helper import load_string
import copy


class Mergable(object):
    __metaclass__ = abc.ABCMeta

    def __init__(self,data=None):
        if data:
            self.merge(data)

    @abc.abstractmethod
    def can_merge(self, data):
        raise NotImplementedError()

    @abc.abstractmethod
    def _merge(self,data):
        raise NotImplementedError()
    
    @abc.abstractmethod
    def copy(self):
        return copy.deepcopy(self)

    @classmethod
    @abc.abstractmethod
    def empty(cls):
        raise NotImplementedError()

    @classmethod    
    def make_mergable_if_possible(cls,data):
        if isinstance(data, dict):
            return ConfigDict(data=data)
        elif isiterable(data):
            return ConfigList([cls.make_mergable_if_possible(i) for i in data])
        else:
            return data

    def merge(self, *args):
        """
        Merges this instance with new instances, in-place.
        returns the self.empty(), if the empty string or None was passed as data.
        """
        for data in args:
            to_merge = None
            if isinstance(data, str):
                to_merge = load_string(data)
            else:
                to_merge = data
            if self.can_merge(to_merge):
                self._merge(to_merge)
            else:
                raise ConfigurationMergeError('Cannot merge myself:%s with %s. data: %s' % (type(self),type(data),data))

    def _ensure_namespaces(self,*namespaces):
        if namespaces:
            ns = namespaces[0]
            if ns not in self:
                self[ns] = ConfigNamespace()
            return self.__getattr__(ns)._ensure_namespaces(*namespaces[1:])
        else:
            return self


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
                    self[k] = Mergable.make_mergable_if_possible(copy.deepcopy(v))

    def __getattr__(self, key):
        if key in self:
            return self.get(key)
        raise ConfigKeyError(key)

    def __setattr__(self, key, value):
        if not key in self:
            self.__dict__[key] = value
        else:
            self[key] = value

    def copy(self):
        return ConfigDict(self)

    @classmethod
    def empty(cls):
        return cls()

class ConfigNamespace(ConfigDict, Mergable):
    def __init__(self, data=None):
        ConfigDict.__init__(self)
        Mergable.__init__(self, data=data)
        

class ConfigList(list, Mergable):

    def __init__(self, data=None):
        list.__init__(self)
        Mergable.__init__(self, data=data)

    def can_merge(self, data):
        return data and hasattr(data, '__iter__')

    def _merge(self, data):
        for item in data:
            if item not in self:
                self.append(item)

    def copy(self):
        return ConfigList(self)

    @classmethod
    def empty(cls):
        return cls()
