
from pymlconf.mergable import MergableDict
from pymlconf.ConfigNode import ConfigNode
from pymlconf.errors import ConfigKeyError
from pymlconf.yaml_helper import load_string


class ConfigDict(MergableDict, ConfigNode):

    def __init__(self, data=None):

        def _normalize(d):
            for k, v in list(d.items()):
                if isinstance(v, dict) and not isinstance(v, ConfigDict):
                    yield k, ConfigDict(v)
                else:
                    yield k, v

        if data:
            if isinstance(data, ConfigDict):
                MergableDict.__init__(self, data)
            else:
                MergableDict.__init__(self, _normalize(data))
        else:
            MergableDict.__init__(self)
        ConfigNode.__init__(self)

    def merge(self, *args):
        for data in args:
            if isinstance(data, str):
                data = load_string(data)
            super(ConfigDict, self).merge(ConfigDict(data))

    def __getattr__(self, key):
        if key in self:
            return self.get(key)
        raise ConfigKeyError(key)

    def __setattr__(self, key, value):
        if not key in self:
            self.__dict__[key] = value
        else:
            self[key] = value

    def _ensure_namespaces(self, *namespaces):
        if namespaces:
            ns = namespaces[0]
            if ns not in self:
                self[ns] = ConfigDict()
            return self.__getattr__(ns)._ensure_namespaces(*namespaces[1:])
        else:
            return self

    def copy(self):
        return ConfigDict(MergableDict.copy(self))
