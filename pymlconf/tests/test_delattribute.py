from pymlconf import Root


def test_delattribute():
    root = Root('''
        app:
          name: MyApp
    ''')

    assert hasattr(root.app, 'name')
    del root.app.name
    assert not hasattr(root.app, 'name')

