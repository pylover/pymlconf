# noinspection PyUnresolvedReferences
class ConfigurationError(Exception):
    def __init__(self, message):
        super(ConfigurationError,self).__init__(message)

class ConfigKeyError(ConfigurationError, AttributeError):
    def __init__(self, key):
        AttributeError.__init__(self)
        ConfigurationError.__init__(self,'Config key was not found: "%s"' % key)

class ConfigurationMergeError(ConfigurationError, ValueError):
    def __init__(self, message):
        super(ConfigurationError,self).__init__(message)

class ConfigFileNotFoundError(ConfigurationError):
    def __init__(self, filename):
        ConfigurationError.__init__(self,'Config File not found: "%s"' % filename)
