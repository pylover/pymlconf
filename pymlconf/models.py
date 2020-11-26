import abc
import copy
from collections.abc import Iterable
from collections import OrderedDict
from os import path

from .errors import ConfigurationAlreadyInitializedError, \
    ConfigurationNotInitializedError
from . import yamlhelper


def isiterable(o):
    if isinstance(o, (bytes, str, type)):
        return False
    return isinstance(o, Iterable)


class Mergable(metaclass=abc.ABCMeta):
    """Base class for all configuration nodes.

    So all configuration nodes are mergable.

    :param data: Initial value to constract a mergable instance. It can be
                 ``yaml string`` or python dictionary. default: None.
    :type data: list or dict

    :param context: dictionary to format the yaml before parsing in
                    pre-processor.
    :type context: dict

    """

    def __init__(self, data=None, context=None):
        self.context = context if context else {}
        if data:
            self.merge(data)

    @abc.abstractmethod
    def canmerge(self, data):  # pragma: no cover
        """Determine whenever can merge with the passed argument or not.

        :param data: An object to test.
        :type data: any

        :returns: bool
        """
        raise NotImplementedError()

    @abc.abstractmethod
    def _merge(self, data):  # pragma: no cover
        raise NotImplementedError()

    @abc.abstractmethod
    def dump(self):  # pragma: no cover
        """Return a python dictionary or list from current config instance."""
        raise NotImplementedError()

    @abc.abstractmethod
    def copy(self):  # pragma: no cover
        """Return a copy of current config instance.

        :returns: :class:`.Mergable`
        """
        raise NotImplementedError()

    @classmethod
    def make_mergable_if_possible(cls, data, context):
        """Make an object mergable if possible.

        Returns the virgin object if cannot convert it to a mergable instance.

        :returns: :class:`.Mergable` or type(data)
        """
        if isinstance(data, dict):
            return MergableDict(data=data, context=context)
        elif isiterable(data):
            return MergableList(
                data=[cls.make_mergable_if_possible(i, context) for i in data],
                context=context
            )
        else:
            return data

    def merge(self, *args):
        """Merge this instance with new instances, in-place.

        :param args: Configuration values to merge with current instance.
        :type args: iterable

        """
        for data in args:
            if isinstance(data, str):
                tomerge = yamlhelper.loads(data, self.context)
                if not tomerge:
                    continue
            else:
                tomerge = data

            if not self.canmerge(tomerge):
                raise TypeError(
                    'Cannot merge myself:%s with %s. data: %s'
                    % (type(self), type(data), data)
                )

            self._merge(tomerge)


class MergableDict(OrderedDict, Mergable):
    """Configuration node that represents python dictionary data."""

    def __init__(self, *args, **kwargs):
        OrderedDict.__init__(self)
        Mergable.__init__(self, *args, **kwargs)

    def canmerge(self, data):
        return data is not None and isinstance(data, dict)

    def _merge(self, data):
        for k in list(data.keys()):
            v = data[k]

            if k in self \
                    and isinstance(self[k], Mergable) \
                    and self[k].canmerge(v):
                self[k].merge(v)
            else:
                if isinstance(v, Mergable):
                    self[k] = v.copy()
                else:
                    self[k] = Mergable.make_mergable_if_possible(
                        copy.deepcopy(v),
                        self.context
                    )

    def __getattr__(self, key):
        """Find and return ``key`` in self.

        Raise :class:`AttributeError` if not any.
        """
        if key in self:
            return self.get(key)
        raise AttributeError(key)

    def __setattr__(self, key, value):
        """Set an item.

        Same as ``self[key] = value``.
        """
        if key not in self:
            self.__dict__[key] = value
        else:
            self[key] = value

    def __delattr__(self, key):
        """Delete an item.

        Same as ``del self[key]``.
        """
        if key in self:
            del self[key]
            return

        super().__delattr__(key)

    def copy(self):
        return MergableDict(self, context=self.context)

    def dump(self):
        return {
            k: v.dump() if isinstance(v, Mergable) else v
            for k, v in self.items()
        }


class ConfigurationNamespace(MergableDict):
    """Configuration node that represents the configuration namespace node."""


class MergableList(list, Mergable):
    """Configuration node that represents the python list data."""

    def __init__(self, *args, **kwargs):
        list.__init__(self)
        Mergable.__init__(self, *args, **kwargs)

    def canmerge(self, data):
        return data and hasattr(data, '__iter__')

    def _merge(self, data):
        del self[:]
        self.extend(data)

    def copy(self):
        return MergableList(self, context=self.context)

    def dump(self):
        return [
            i.dump() if isinstance(i, Mergable) else i
            for i in self
        ]


class Root(MergableDict):
    """The main class which exposes pymlconf package.

    Example::

        from pymlconf import Root
        from os import path
        config =  Root('''
            server:
                host: localhost
                port: 4455
        ''')

        print config.server.host
        print config.server.port

    """

    def loadfile(self, filename):
        """Load yaml configuration file and merge it by current instance.

        :param filename: filename to load and merge into existing configuration
                         instance
        """
        if not path.exists(filename):
            raise FileNotFoundError(filename)

        loadedyaml = yamlhelper.load(filename, self.context)
        if loadedyaml:
            self.merge(loadedyaml)

    def dumps(self):
        """Encode the instance as YAML String.

        .. versionadded:: 2.3

        """
        return yamlhelper.dumps(self.dump())


class DeferredRoot:
    _instance = None

    def __getattr__(self, key):
        """Get an attribute of underlying deferred configuration instance."""
        return getattr(
            object.__getattribute__(self, '__class__')._getinstance(),
            key
        )

    def __setattr__(self, key, value):
        """Set an attribute of underlying deferred configuration instance."""
        setattr(
            object.__getattribute__(self, '__class__')._getinstance(),
            key,
            value
        )

    @classmethod
    def _getinstance(cls):
        if cls._instance is None:
            raise ConfigurationNotInitializedError(
                'Configuration manager object is not initialized yet.'
            )
        return cls._instance

    def initialize(self, init_value, context=None, force=False):
        """Initialize the configuration manager.

        :param force: force initialization even if it's already initialized
        :return:
        """
        if not force and self._instance is not None:
            raise ConfigurationAlreadyInitializedError(
                'Configuration manager object is already initialized.'
            )

        self.__class__._instance = Root(init_value, context=context)
