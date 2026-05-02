import copy

from . import yaml_


class Meld(dict):
    def __init__(self, data=None, file=None):
        super().__init__()
        if data is not None:
            self |= data

        if file:
            self.load(file)

    def __ior__(self, data):
        if isinstance(data, str):
            data = yaml_.load(data)
            docopy = False
        else:
            docopy = True

        if not isinstance(data, dict):
            raise TypeError(
                'Only dict and or it\'s subclasses are allowed, '
                f'given: {type(data)}')

        if docopy:
            data = copy.deepcopy(data)

        for k in data:
            mine = self.get(k)
            other = data.get(k)
            if isinstance(mine, Meld):
                mine |= other
            elif isinstance(other, dict):
                self[k] = Meld(other)
            else:
                self[k] = other

        return self

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

    def load(self, file):
        self |= yaml_.loadfile(file)
