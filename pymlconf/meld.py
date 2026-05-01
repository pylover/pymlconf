import copy

from . import yaml_


class Meld(dict):
    def __init__(self, data):
        super().__init__()
        self.mergein(data)

    def mergein(self, data):
        if isinstance(data, str):
            data = yaml_.load(data)
            docopy = False
        else:
            docopy = True

        if not isinstance(data, dict):
            raise TypeError(f'Only dict and or it\'s subclasses are allowed')

        if docopy:
            data = copy.deepcopy(data)

        for k in data:
            mine = self.get(k)
            other = data.get(k)
            if isinstance(mine, Meld):
                mine.mergein(other)
            else:
                self[k] = other

    def __getattr__(self, key):
        if key not in self:
            raise AttributeError(key)

        return self[key]

    def __setattr__(self, key, value):
        super().__setitem__(key, value)

    def __delattr__(self, key):
        if key not in self:
            raise AttributeError(key)

        del self[key]
