
import os

from pymlconf.config_nodes import ConfigDict
from pymlconf.yaml_helper import load_yaml
from pymlconf.compat import basestring
from pymlconf.errors import ConfigFileNotFoundError
import warnings

IGNORE = 0
ERROR = 1
WARNING = 2
missing_file_behaviors = [IGNORE,
                          ERROR,
                          WARNING]


class ConfigManager(ConfigDict):
    """
    The main class which exposes pymlconf package.

    Example::

        from pymlconf import ConfigManager
        from os import path
        config =  ConfigManager('''
            server:
                host: localhost
                port: 4455
            ''','conf','builtins/defaults.conf')

        print config.server.host
        print config.server.port

    """

    default_extension = ".conf"

    def __init__(self, init_value=None, dirs=None, files=None, filename_as_namespace=True,
                 extension='.conf', root_file_name='root', missing_file_behavior=WARNING, encoding='utf-8',
                 context=None, builtin=None):
        """
        :param init_value: Initial configuration value that you can pass it before reading the files and directories.can
                           be 'yaml string' or python dictionary.
        :type init_value: str or dict

        :param dirs: Python list  or a string that contains semi-colon separated list of directories which contains
                     configuration files with specified extension(default \*.conf).
        :type dirs: str or list

        :param files: Python list  or a string that contains semi-colon separated list of files which contains yaml
                      configuration entries.
        :type files: str or list

        :param filename_as_namespace: when loading dirs, use the filename as a namespace. default: true.
        :type filename_as_namespace: bool

        :param extension: File extension to search for configuration files, in dirs parameter, default '.conf'
        :type extension: str

        :param root_file_name: Filename to treat as root configuration file, so it loads first, and do not uses the
                               filename as namespaces.
        :type root_file_name: str

        :param missing_file_behavior: What should do when a file was not found, set to 0 (zero) to ignore. default to
                                      ``warning(2)``
        :type missing_file_behavior: integer 0:ignore, 1:throw error, 2:warning

        :param context: dictionary to format the yaml before parsing in pre processor.
        :type context: dict

        :param builtin: Same as the ``init_value``, but it will be loaded before the loading the ``init_value``,
                        helps to implement builtin config pattern.
        :type builtin: str or dict

        .. versionadded:: 0.6.0a

           The ``builtin`` parameter was added.

        """

        self.default_extension = extension
        self.root_file_name = root_file_name
        self.missing_file_behavior = missing_file_behavior
        self.encoding = encoding

        # Loading the instance with built-in config
        super(ConfigManager, self).__init__(data=builtin, context=context)

        # Loading init_value
        if init_value:
            self.merge(init_value)

        if dirs:
            self.load_dirs(dirs, filename_as_namespace=filename_as_namespace)

        if files:
            self.load_files(files)

    def load_files(self, files, filename_as_namespace=False):
        """
        load files which contains yaml configuration entries.and merge it by current ConfigManager instance

        :param files: files to load and merge into existing configuration instance
        :type files: list

        :param filename_as_namespace: when loading files, use the filename as a namespace. default: false.
        :type filename_as_namespace: bool

        """
        files = [f.strip() for f in files.split(';')] if isinstance(files, basestring) else files
        for f in files:
            if not os.path.exists(f):
                if self.missing_file_behavior == ERROR:
                    raise ConfigFileNotFoundError(f)
                elif self.missing_file_behavior == WARNING:
                    warnings.warn('File not found: %s' % f)
                continue

            if filename_as_namespace:
                assert f.endswith(self.default_extension), \
                    'Invalid configuration filename.expected: ns1.ns2.*%s' % self.default_extension
                namespace = os.path.splitext(os.path.split(f)[1])[0]
                if namespace == self.root_file_name:
                    node = self
                else:
                    node = self._ensure_namespaces(*namespace.split('.'))
            else:
                node = self

            loaded_yaml = load_yaml(f, self.context, encoding=self.encoding)
            if loaded_yaml:
                node.merge(loaded_yaml)

    loadfiles = load_files

    def load_dirs(self, dirs, filename_as_namespace=True):
        """
        load directories which contains configuration files with specified extension, and merge it by current
        ConfigManager instance

        :param dirs: Dirs to search for configuration files.
        :type dirs: list,string

        :param filename_as_namespace: when loading dirs, use the filename as a namespace. default: true.
        :type filename_as_namespace: bool

        """

        dirs = [d.strip() for d in dirs.split(';')] if isinstance(dirs, basestring) else dirs
        candidate_files = []
        for d in dirs:
            full_paths = (os.path.join(d, f) for f in os.listdir(d))
            conf_files = (f for f in full_paths if
                          (os.path.isfile(f) or os.path.islink(f)) and f.endswith(self.default_extension))
            candidate_files.extend(sorted(conf_files))

        root_file_name = None
        for f in candidate_files:
            if f.endswith(self.root_file_name + self.default_extension):
                root_file_name = f
                break

        # remove and insert root.conf in index 0.
        if root_file_name:
            candidate_files = [root_file_name] + [f for f in candidate_files if f != root_file_name]

        self.load_files(candidate_files, filename_as_namespace=filename_as_namespace)

    loaddirs = load_dirs
