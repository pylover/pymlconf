
from ConfigNode import ConfigNode
from mergable import MergableList

class ConfigList(MergableList, ConfigNode):

    def copy(self):
        return ConfigList(MergableList.copy(self))

