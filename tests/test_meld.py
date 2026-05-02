import os

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


def test_meld_root():
    m = Meld('''
      foo:
        a: 1
    ''')

    m |= Meld(root='foo', data='''
      b: 2
    ''')

    assert m.foo.a == 1
    assert m.foo.b == 2

    m |= Meld(root='bar', data='''
      c: 3
    ''')
    assert m.bar.c == 3


def test_meld_setattr():
    m = Meld()
    m.foo = 'bar'
    assert m.foo == 'bar'

    m.bar = dict(
        a=1,
        baz=dict(
            b=2,
            c=3
        )
    )
    assert isinstance(m.bar, Meld)
    assert isinstance(m.bar.baz, Meld)
    assert m.bar.a == 1
    assert m.bar.baz.b == 2
    assert m.bar.baz.c == 3


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


def test_include(mktmpfile):
    baz = mktmpfile(name='baz.yml', content='''
      baz: 1272
    ''')
    foo = mktmpfile(name='foo.yml', content='''
      foo:
        a: 1
        b: 2
    ''')
    bar = mktmpfile(name='bar.yml', content=f'''
      bar:
        a: 11
        b: !include {baz}
    ''')
    m = Meld()

    m |= f'!include {foo}'
    m |= f'!include {bar}'
    assert m.foo.a == 1
    assert m.foo.b == 2
    assert m.bar.a == 11
    assert m.bar.b.baz == 1272


def test_env():
    user = os.environ['USER']
    m = Meld('foo: !env USER')
    assert m.foo == user


def test_shell():
    m = Meld('foo: !shell echo hello')
    assert m.foo == 'hello'


def test_dump(mktmpfile):
    qux = mktmpfile(content='qux')
    user = os.environ['USER']
    m = Meld(f'''
      foo:
        a: !shell echo hello
        b: !env USER
        c: !include {qux}
    ''')

    assert m.dump() == \
        'foo:\n' \
        '  a: hello\n' \
        f'  b: {user}\n' \
        '  c: qux\n'


def test_base64():
    foo = Meld('''
      foo: !!binary YWJj\n
    ''')

    assert foo.foo == b'abc'
