
class ConfigurationError(Exception):
    pass


class ConfigurationNotInitializedError(ConfigurationError):
    pass


class ConfigurationAlreadyInitializedError(ConfigurationError):
    pass
