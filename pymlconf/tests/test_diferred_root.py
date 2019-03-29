import pytest

from pymlconf import DeferredRoot
from pymlconf.errors import ConfigurationNotInitializedError, \
    ConfigurationAlreadyInitializedError


class TestDiferredRoot:

    def test_deferred_config_manager(self):
        context = dict(
            c=3
        )
        config = '''
            a: 1
            b:
              - 1
        '''

        root = DeferredRoot()
        with pytest.raises(ConfigurationNotInitializedError):
            root.attr

        root.initialize(config, context)

        with pytest.raises(ConfigurationAlreadyInitializedError):
            root.initialize(config)

        root.merge('''
            c: %(c)s
        ''')

        assert root.a == 1
        assert root.b == [1]
        assert root.c == 3

        root.d = [1, 2]
        assert [1, 2] == root.d

