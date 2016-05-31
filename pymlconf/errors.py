from os.path import abspath


class ConfigurationError(Exception):
    def __init__(self, message):
        super(ConfigurationError, self).__init__(message)


class ConfigKeyError(ConfigurationError, AttributeError):
    def __init__(self, key):
        AttributeError.__init__(self)
        ConfigurationError.__init__(self, 'Config key was not found: "%s"' % key)


class ConfigurationMergeError(ConfigurationError, ValueError):
    def __init__(self, message):
        super(ConfigurationError, self).__init__(message)


class ConfigFileNotFoundError(ConfigurationError):
    def __init__(self, filename):
        ConfigurationError.__init__(self, 'Config File not found: "%s"' % abspath(filename))


class ConfigFileSyntaxError(ConfigurationError):
    def __init__(self, filename, inner_exception):
        ConfigurationError.__init__(self, '%s\nFilename: %s"'
                                    % (str(inner_exception), abspath(filename)))


class ConfigurationNotInitializedError(ConfigurationError):
    pass


class ConfigurationAlreadyInitializedError(ConfigurationError):
    pass
