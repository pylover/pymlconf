
from pymlconf.models import Mergable, MergableList, MergableDict, \
    ConfigurationNamespace, Root
from pymlconf.errors import ConfigurationError, ConfigKeyError, \
    ConfigurationAlreadyInitializedError, ConfigurationNotInitializedError
from pymlconf.proxy import DeferredConfigManager


__version__ = '0.8.9'

