import unittest

from pymlconf import Root


class TestBinary(unittest.TestCase):

    def test_binary(self):
        config = '''
            app:
              name: MyApp
            secret: !!binary YWJj\n
        '''
        cm = ConfigManager(config)

        self.assertEqual(cm.app.name, 'MyApp')
        self.assertEqual(cm.secret, b'abc')


if __name__ == '__main__':  # pragma: no cover
    unittest.main()

