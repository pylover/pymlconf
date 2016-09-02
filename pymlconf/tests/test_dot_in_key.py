
import unittest

from pymlconf import ConfigManager


class DotTestCase(unittest.TestCase):
    def setUp(self):
        self.sample_config = '''

            server.token.salt: 1345

        '''

    def test_dot_in_config_key(self):
        m = ConfigManager(self.sample_config)
        self.assertEqual(m['server.token.salt'], 1345)


if __name__ == '__main__':
    unittest.main()
