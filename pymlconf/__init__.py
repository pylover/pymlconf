"""pymlconf package."""
from .models import Mergable, MergableList, MergableDict, Root, \
    ConfigurationNamespace, DeferredRoot

from .errors import ConfigurationError, ConfigurationAlreadyInitializedError, \
    ConfigurationNotInitializedError


__version__ = '3.0.1'
