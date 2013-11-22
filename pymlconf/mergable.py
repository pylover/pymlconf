
from pymlconf.yaml_helper import load_string
import copy

class Mergable(object):

    def __init__(self,data=None):
        if data:
            self.merge(data)

    def can_merge(self, data):
        raise NotImplementedError()

    def merge(self, *args):
        """
        Merges this instance with new instances, in-place.
        returns the self.empty(), if the empty string or None was passed as data.
        """
        for data in args:
            to_merge = None
            if isinstance(data, str):
                to_merge = load_string(data)
            else:
                to_merge = data
            if self.can_merge(to_merge):
                self._merge(to_merge)
            else:
                raise ValueError('Cannot merge myself:%s with %s. data: %s' % (type(self),type(data),data))
    
    def _merge(self,data):
        raise NotImplementedError()
    
    @classmethod
    def empty(self):
        raise NotImplementedError()
        
    def copy(self):
        return copy.deepcopy(self)

    def _ensure_namespaces(self, *namespaces):
        from pymlconf import ConfigDict
        if namespaces:
            ns = namespaces[0]
            if ns not in self:
                self[ns] = ConfigDict()
            return self.__getattr__(ns)._ensure_namespaces(*namespaces[1:])
        else:
            return self