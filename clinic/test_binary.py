from pymlconf import Root


def test_binary():
    root = Root('''
        app:
          name: MyApp
        secret: !!binary YWJj\n
    ''')

    assert root.app.name == 'MyApp'
    assert root.secret == b'abc'
