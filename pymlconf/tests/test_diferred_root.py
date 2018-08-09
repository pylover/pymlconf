import unittest

from pymlconf import DeferredRoot
from pymlconf.errors import ConfigurationNotInitializedError, \
    ConfigurationAlreadyInitializedError


class TestDiferredRoot(unittest.TestCase):

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
        with self.assertRaises(ConfigurationNotInitializedError):
            root.attr

        root.initialize(config, context)

        with self.assertRaises(ConfigurationAlreadyInitializedError):
            root.initialize(config)

        root.merge('''
            c: %(c)s
        ''')

        self.assertEqual(root.a, 1)
        self.assertEqual(root.b, [1])
        self.assertEqual(root.c, 3)


if __name__ == '__main__':
    unittest.main()