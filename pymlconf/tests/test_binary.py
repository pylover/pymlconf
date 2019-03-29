from pymlconf import Root


class TestBinary:

    def test_binary(self):
        root = Root('''
            app:
              name: MyApp
            secret: !!binary YWJj\n
        ''')

        assert root.app.name == 'MyApp'
        assert root.secret == b'abc'

