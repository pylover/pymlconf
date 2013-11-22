
import os

from pymlconf.config_nodes import ConfigDict
from pymlconf.yaml_helper import load_yaml
from pymlconf.compat import basestring

class ConfigManager(ConfigDict):
    """
    The main class to using the pymlconf package.

    Parameters::
        init_value: Initial configuration value that you can pass it before reading the files and directories.can be 'yaml string' or python dictionary.

        dirs: Python list  or a string that contains comma separated list of directories which contains config files with specified extension(default *.conf).

        files: Python list  or a string that contains comma separated list of files which contains yaml config entries.

        filename_as_namespace: when loading dirs, use the filename as a namespace.

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
    # Operations
    def __init__(self, init_value=None, dirs=None, files=None, filename_as_namespace=True,
                 extension='.conf',root_file_name='root'):
        super(ConfigManager,self).__init__(data=init_value)
        self.default_extension = extension
        self.root_file_name = root_file_name
        if dirs:
            if isinstance(dirs, basestring):
                dirs = [d.strip() for d in dirs.split(';')]
            self.load_dirs(dirs, filename_as_namespace=filename_as_namespace)
            
        if files:
            if isinstance(files, basestring):
                files = [f.strip() for f in files.split(';')]
            self.load_files(files)


    def load_files(self, files, filename_as_namespace=False):
        """
        load files which contains yaml config entries.and merge it by current ConfigManager instance
        """
        for f in files:
            if not os.path.exists(f):
                continue
            if filename_as_namespace:
                assert f.endswith(self.default_extension), 'Invalid config filename.expected: ns1.ns2.*%s' % self.default_extension
                namespace = os.path.splitext(os.path.split(f)[1])[0]
                if namespace == self.root_file_name:
                    node = self
                else:
                    node = self._ensure_namespaces(*namespace.split('.'))
            else:
                node = self
            node.merge(load_yaml(f))

    def load_dirs(self, dirs, filename_as_namespace=True):
        """
        load directories which contains config files with specified extension, and merge it by current ConfigManager instance
        """
        candidate_files = []
        for d in dirs:
            full_paths = (os.path.join(d, f) for f in os.listdir(d))
            conf_files = (f for f in full_paths if (os.path.isfile(f) or os.path.islink(f)) and f.endswith(self.default_extension))
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
