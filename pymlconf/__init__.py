
from .models import Mergable, MergableList, MergableDict, Root, \
    ConfigurationNamespace
from .errors import ConfigurationError, ConfigKeyError, \
    ConfigurationAlreadyInitializedError, ConfigurationNotInitializedError
from .proxy import DeferredRoot


__version__ = '1.0.0dev'

