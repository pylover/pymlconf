import unittest
from pymlconf import DeferredConfigManager
from pymlconf.compat import TestCase
from pymlconf.errors import ConfigurationNotInitializedError, \
    ConfigurationAlreadyInitializedError


class TestConfigManager(TestCase):
    def setUp(self):
        self.builtin_config = """
            version: 2.5
            general:
                name: albatross
        """

    def test_deferred_config_manager(self):

        a_date = '2014/12/01'
        cm = DeferredConfigManager()
        self.assertRaises(
            ConfigurationNotInitializedError,
            lambda: cm.version
        )

        cm.load(init_value=self.builtin_config, context=dict(date=a_date))

        self.assertRaises(
            ConfigurationAlreadyInitializedError,
            lambda: cm.load(init_value=self.builtin_config)
        )

        cm.merge("""
a_date: %(date)s
        """)
        self.assertEqual(cm.version, 2.5)
        cm.version = 2.6
        self.assertEqual(cm.version, 2.6)
        self.assertEqual(cm.a_date, a_date)
        self.assertEqual(cm.general.name, 'albatross')


if __name__ == '__main__':
    unittest.main()
