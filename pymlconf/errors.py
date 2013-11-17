


class ConfigurationError(Exception):
    def __init__(self, message):
        super(ConfigurationError,self).__init__(message)

class ConfigKeyError(ConfigurationError, AttributeError):
    def __init__(self, key):
        AttributeError.__init__(self)
        ConfigurationError.__init__(self,'Config key was not found: "%s"' % key)
