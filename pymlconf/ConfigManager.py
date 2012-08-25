

from ConfigDict import ConfigDict
from yaml_helper import load_yaml, load_string
import os

class ConfigManager(ConfigDict):
    """
    The main class to using the pymlconf package.
        
    Parameters::
        init_value: Initial configuration value that you can pass it before reading the files and directories.can be 'yaml string' or python dictionary.
            
        dirs: Python list  or a string that contains comma separated list of directories which contains config files with \*.conf extension. 
        
        files: Python list  or a string that contains comma separated list of files which contains yaml config entries.
                
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
    # Operations
    def __init__(self, init_value=None, dirs=None, files=None):
        ConfigDict.__init__(self)
        if init_value:
            if isinstance(init_value, (list, tuple)):
                for iv in init_value:
                    self.merge(iv)
            elif isinstance(init_value, dict):
                self.merge(init_value)
            elif isinstance(init_value, basestring):
                self.merge(load_string(init_value))
            else:
                raise Exception("Invalid config value")
        if dirs:
            if isinstance(dirs, basestring):
                dirs = [d.strip() for d in  dirs.split(';')]
            self.load_dirs(*dirs)
        if files:
            if isinstance(files, basestring):
                files = [f.strip() for f in  files.split(';')]
            self._load_files(files)
    
    
    def load_files(self, *files):
        self._load_files(files)
        
    def _load_files(self, files, filename_as_namespace=False):
        """
        load files which contains yaml config entries.and merge it by current ConfigManager instance
        """
        for f in files:
            if not os.path.exists(f):
                continue
            if filename_as_namespace:
                assert f.endswith('.conf'), 'Invalid config filename.expected: ns1.ns2.*.conf'
                namespace = os.path.splitext(os.path.split(f)[1])[0]
                if namespace == 'root':
                    node = self
                else:
                    node = self._ensure_namespaces(*namespace.split('.'))
            else:
                node = self
            node.merge(load_yaml(f))
    
    def load_dirs(self, *dirs):
        """
        load directories which contains config files with \*.conf extension, and merge it by current ConfigManager instance        
        """
        candidate_files = []       
        for d in dirs:
            for (path, dirs, files) in os.walk(d):
                for f in files:
                    if f.endswith('.conf'):
                        candidate_files.append(os.path.join(path, f))
        self._load_files(candidate_files, filename_as_namespace=True)


