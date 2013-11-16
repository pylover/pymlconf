
from pymlconf.config_node import ConfigNode
from pymlconf.mergable import MergableList


class ConfigList(MergableList, ConfigNode):

    def copy(self):
        return ConfigList(MergableList.copy(self))
