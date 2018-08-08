import unittest

from pymlconf import Root


class TestBinary(unittest.TestCase):

    def test_binary(self):
        root = Root('''
            app:
              name: MyApp
            secret: !!binary YWJj\n
        ''')

        self.assertEqual(root.app.name, 'MyApp')
        self.assertEqual(root.secret, b'abc')


if __name__ == '__main__':  # pragma: no cover
    unittest.main()

