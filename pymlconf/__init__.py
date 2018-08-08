
from .models import Mergable, MergableList, MergableDict, Root, \
    ConfigurationNamespace, DeferredRoot
# FIXME: remove all errors
from .errors import ConfigurationError, ConfigKeyError, \
    ConfigurationAlreadyInitializedError, ConfigurationNotInitializedError


__version__ = '1.0.0dev'

