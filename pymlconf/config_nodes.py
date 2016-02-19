
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

    def __init__(self, data=None, context=None):
        """
        :param data: Initial value to constract a mergable instance. default: None.
        :type data: list or dict
        """
        self.context = context if context else {}
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
    def _merge(self, data):
        raise NotImplementedError()

    @abc.abstractmethod
    def copy(self):
        """
        When implemented, returns copy of current config instance.

        :returns: :class:`.Mergable`
        """
        #return copy.deepcopy(self)
        raise NotImplementedError()

    @classmethod
    @abc.abstractmethod
    def empty(cls):
        """
        When implemented, returns an empty instance of drived :class:`.Mergable` class.

        :returns: :class:`.Mergable`
        """
        raise NotImplementedError()

    @classmethod
    def make_mergable_if_possible(cls, data, context):
        """
        Makes an object mergable if possible. Returns the virgin object if cannot convert it to a mergable instance.

        :returns: :class:`.Mergable` or type(data)

        """
        if isinstance(data, dict):
            return ConfigDict(data=data,
                              context=context)
        elif isiterable(data):
            return ConfigList(data=[cls.make_mergable_if_possible(i, context) for i in data],
                              context=context)
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
                to_merge = load_string(data, self.context)
                if not to_merge:
                    continue
            else:
                to_merge = data

            if self.can_merge(to_merge):
                self._merge(to_merge)
            else:
                raise ConfigurationMergeError(
                    'Cannot merge myself:%s with %s. data: %s' % (type(self), type(data), data))

    def _ensure_namespaces(self, *namespaces):
        if namespaces:
            ns = namespaces[0]
            if ns not in self:
                self[ns] = ConfigNamespace(context=self.context)
            return self.__getattr__(ns)._ensure_namespaces(*namespaces[1:])
        else:
            return self


class ConfigDict(OrderedDict, Mergable):
    """
    Configuration node that represents python dictionary data.
    """

    def __init__(self, *args, **kwargs):
        OrderedDict.__init__(self)
        Mergable.__init__(self, *args, **kwargs)

    def can_merge(self, data):
        return data is not None and isinstance(data, dict)

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
                    self[k] = Mergable.make_mergable_if_possible(copy.deepcopy(v), self.context)

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
        return ConfigDict(self, context=self.context)

    @classmethod
    def empty(cls):
        return cls()


class ConfigNamespace(ConfigDict, Mergable):
    """
    Configuration node that represents the configuration namespace node.
    """

    def __init__(self, *args, **kwargs):
        ConfigDict.__init__(self)
        Mergable.__init__(self, *args, **kwargs)


class ConfigList(list, Mergable):
    """
    Configuration node that represents the python list data.
    """

    def __init__(self, *args, **kwargs):
        list.__init__(self)
        Mergable.__init__(self, *args, **kwargs)

    def can_merge(self, data):
        return data and hasattr(data, '__iter__')

    def _merge(self, data):
        del self[:]
        self.extend(data)
        # for item in data:
        #     if item not in self:
        #         self.append(item)

    def copy(self):
        return ConfigList(self, context=self.context)

    @classmethod
    def empty(cls):
        return cls()
