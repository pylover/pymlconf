
import abc
from pymlconf.errors import ConfigKeyError, ConfigurationMergeError
from pymlconf.compat import OrderedDict, isiterable
from pymlconf.yaml_helper import load_string
import copy


# noinspection PyUnresolvedReferences,PyUnresolvedReferences
class Mergable(object):
    """ Base class for all configuration nodes, so all configuration nodes are mergable
    """
    __metaclass__ = abc.ABCMeta

    def __init__(self,data=None):
        """
        :param data: Initial value to constract a mergable instance. default: None.
        :type data: list or dict
        """
        if data:
            self.merge(data)

    @abc.abstractmethod
    def can_merge(self, data):
        """
        Determines whenever can merge with the passed argument or not.

        :param data: An object to test.
        :type data: any

        :returns: bool
        """
        raise NotImplementedError()

    @abc.abstractmethod
    def _merge(self,data):
        raise NotImplementedError()

    @abc.abstractmethod
    def copy(self):
        """
        When implemented, returns copy of current config instance.

        :returns: :class:`.Mergable`
        """
        return copy.deepcopy(self)

    @classmethod
    @abc.abstractmethod
    def empty(cls):
        """
        When implemented, returns an empty instance of drived :class:`.Mergable` class.

        :returns: :class:`.Mergable`
        """
        raise NotImplementedError()

    @classmethod
    def make_mergable_if_possible(cls,data):
        """
        Makes an object mergable if possible. Returns the virgin object if cannot convert it to a mergable instance.

        :returns: :class:`.Mergable` or type(data)

        """
        if isinstance(data, dict):
            return ConfigDict(data=data)
        elif isiterable(data):
            return ConfigList([cls.make_mergable_if_possible(i) for i in data])
        else:
            return data

    def merge(self, *args):
        """
        Merges this instance with new instances, in-place.

        :param \*args: Configuration values to merge with current instance.
        :type \*args: iterable

        """
        for data in args:
            if isinstance(data, str):
                to_merge = load_string(data)
                if not to_merge:
                    continue
            else:
                to_merge = data

            if self.can_merge(to_merge):
                self._merge(to_merge)
            else:
                raise ConfigurationMergeError('Cannot merge myself:%s with %s. data: %s' % (type(self),type(data),data))

    def _ensure_namespaces(self, *namespaces):
        if namespaces:
            ns = namespaces[0]
            if ns not in self:
                self[ns] = ConfigNamespace()
            # noinspection PyProtectedMember
            return self.__getattr__(ns)._ensure_namespaces(*namespaces[1:])
        else:
            return self


class ConfigDict(OrderedDict, Mergable):
    """
    Configuration node that represents python dictionary data.
    """

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
    """
    Configuration node that represents the configuration namespace node.
    """
    def __init__(self, data=None):
        ConfigDict.__init__(self)
        Mergable.__init__(self, data=data)


class ConfigList(list, Mergable):
    """
    Configuration node that represents the python list data.
    """
    def __init__(self, data=None):
        # noinspection PyTypeChecker
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
