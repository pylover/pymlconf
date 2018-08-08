import os

from .config_nodes import ConfigDict
from .errors import ConfigFileNotFoundError
from .yaml_helper import load_yaml


class Root(ConfigDict):
    """
    The main class which exposes pymlconf package.

    Example::

        from pymlconf import Root
        from os import path
        config =  Root('''
            server:
                host: localhost
                port: 4455
        ''')

        print config.server.host
        print config.server.port

    """


    def __init__(self, init_value=None, context=None):
        """
        :param init_value: Initial configuration value that you can pass it
                           before reading the files and directories.can be
                           'yaml string' or python dictionary.
        :type init_value: str or dict

        :param context: dictionary to format the yaml before parsing in
                        pre-processor.
        :type context: dict

        """

        # Loading the instance with built-in config
        super(ConfigManager, self).__init__(data=init_value, context=context)

    def load_file(self, filename):
        """
        load file which contains yaml configuration entries.and merge it by
        current instance

        :param files: files to load and merge into existing configuration
                      instance
        :type files: list

        """
        if not os.path.exists(filename):
            raise ConfigFileNotFoundError(filename)

        loaded_yaml = load_yaml(f, self.context)
        if loaded_yaml:
            node.merge(loaded_yaml)

