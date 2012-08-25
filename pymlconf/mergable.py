
try:
    from collections import OrderedDict
except:
    from ordereddict import OrderedDict

class Mergable(object):
    
    def _can_merge(self, o):
        raise NotImplementedError()
    
    def merge(self, data):
        raise NotImplementedError()
    
class MergableDict(OrderedDict, Mergable):

    def _can_merge(self, o):
        return isinstance(o, dict)

    def merge(self, data):
        if not data:
            return
        for k in data.keys():
            v = data[k]
            if k in self and isinstance(self[k], Mergable):
                try:
                    self[k].merge(v)
                except AttributeError:
                    raise Exception('config key was not found:%s' % k)
            else:
                self[k] = v
        
    
    def copy(self):
        return MergableDict(OrderedDict.copy(self))
    
    
class MergableList(list, Mergable):

    def _can_merge(self, o):
        return isinstance(o, (list, tuple))

    def merge(self, data):
        for item in data:
            if item not in self:
                self.append(item)
    
    def copy(self):
        return MergableList(list.copy(self))
    
