from pymlconf import Meld


def test_meld():
    m = Meld('''
      foo: bar
      baz:
        a: 1
        b: 2

    ''')

    assert m.foo == 'bar'
    assert m.baz.a == 1

    m |= Meld('''
      baz:
        a: 11
        c: 3
    ''')
    assert m.baz.a == 11
    assert m.baz.b == 2
    assert m.baz.c == 3
