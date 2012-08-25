


class ConfigurationError(Exception):
    pass

class ConfigKeyError(ConfigurationError, AttributeError):
    def __init__(self, key):
        ConfigurationError.__init__(self, 'Config key not found: "%s"', key)
