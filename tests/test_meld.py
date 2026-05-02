import pytest

from pymlconf import Meld


def test_meld_merge():
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

    m |= '''
      foo:
        a: 1
    '''
    assert m.foo.a == 1
    assert m.baz.a == 11

    with pytest.raises(TypeError):
        m |= 'foo'


def test_meld_setattr():
    m = Meld()
    m.foo = 'bar'
    assert m.foo == 'bar'


def test_meld_delattr():
    m = Meld('''
      foo: bar
    ''')

    delattr(m, 'foo')
    with pytest.raises(AttributeError):
        m.foo

    with pytest.raises(AttributeError):
        delattr(m, 'foo')


def test_meld_loadfile(mktmpfile):
    foo = mktmpfile(content='''
      foo:
        a: 1
        b: 2
    ''')

    m = Meld(file=foo)
    assert m.foo.a == 1
    assert m.foo.b == 2

    bar = mktmpfile(content='''
      bar:
        c: 11
        d: 21
    ''')

    with open(bar) as f:
        m.load(f)

    assert m.bar.c == 11
    assert m.bar.d == 21


# def test_include(mktmpfile):
#     foo = mktmpfile(name='foo.yml', content='''
#       foo:
#         a: 1
#         b: 2
#     ''')
#     m = Meld()
#
#     m |= f'!include {foo}'
#     assert m.foo.a == 1
#     assert m.foo.b == 2
