from pymlconf.exceptions import ConfigurationAlreadyInitializedError, ConfigurationNotInitializedError
from pymlconf import ConfigManager


class ObjectProxy(object):
    """
    A simple object proxy to let deferred object's initialize later (for example: just after import):
    This class encapsulates some tricky codes to resolve the proxied object members using the
    `__getattribute__` and '__getattr__'. SO TAKE CARE about modifying the code, to prevent
    infinite loops and stack-overflow situations.

    Module: fancy_module

        deferred_object = None  # Will be initialized later.
        def init():
            global deferred_object
            deferred_object = AnyValue()
        proxy = ObjectProxy(lambda: deferred_object)

    In another module:

        from fancy_module import proxy, init
        def my_very_own_function():
            try:
                return proxy.any_attr_or_method()
            except: ObjectNotInitializedError:
                init()
                return my_very_own_function()

    """

    def __init__(self, resolver):
        object.__setattr__(self, '_resolver', resolver)

    @property
    def proxied_object(self):
        o = object.__getattribute__(self, '_resolver')()
        # if still is none, raise the exception
        if o is None:
            raise ConfigurationNotInitializedError("Configuration manager object is not initialized yet.")
        return o

    def __getattr__(self, key):
        return getattr(object.__getattribute__(self, 'proxied_object'), key)

    def __setattr__(self, key, value):
        setattr(object.__getattribute__(self, 'proxied_object'), key, value)


class DeferredConfigManager(ObjectProxy):
    _instance = None

    def __init__(self):
        super(DeferredConfigManager, self).__init__(
            self._get_instance
        )

    @classmethod
    def _get_instance(cls):
        return cls._instance

    @classmethod
    def _set_instance(cls, v):
        cls._instance = v

    def load(self, config=None, directories=None, files=None, force=False, context=None, **kw):
        """
        Initialize the configuration manager

        :param config: `string` or `dict`
        :param directories: semi-colon separated `string` or `list` of director(y|es)
        :param files: semi-colon separated `string` or `list` of file(s)
        :param force: force initialization even if it's already initialized
        :param context: the pymlconf context
        :return:
        """

        instance = self._get_instance()
        if not force and instance is not None:
            raise ConfigurationAlreadyInitializedError("Configuration manager object is already initialized.")

        instance = ConfigManager(
            config,
            files=files,
            dirs=directories,
            context=context or {},
            **kw
        )
        self._set_instance(instance)
