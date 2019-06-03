import pytest
from os import path

from pymlconf import Root


class TestConfigManager:
    def test_constructor(self):
        context = dict(
            c=3
        )

        builtin = '''
          a:
            a1: 1

          b:
          - 1
          - 2
          - %(c)s
        '''

        root = Root(builtin, context)
        assert root.a.a1 == 1
        assert root.b[0] == 1
        assert root.b[1] == 2
        assert root.b[2] == 3

        root.merge('''
          a:
            a2: 2
        ''')
        assert root.a.a2 == 2

        root.a.a3 = 3
        assert root.a.a1 == 1
        assert root.a.a2 == 2
        assert root.a.a3 == 3

        root.merge('''
          b:
            - 4
        ''')
        assert root.b[0] == 4
        assert len(root.b) == 1

    def test_dot_in_key(self):
        root = Root('''
            server.token.salt: 1345
        ''')

        assert root['server.token.salt'] == 1345
        assert not hasattr(root, 'server')

    def test_load_file(self):
        here = path.dirname(__file__)
        filename = path.join(here, 'files/sample.yml')
        root = Root()
        root.load_file(filename)
        assert root.a.b == 2

        with pytest.raises(FileNotFoundError):
            root.load_file('not/exists')

    def test_callable_context(self):
        def context():
            return dict(c=3)

        root = Root('a: %(c)s', context)
        assert root.a == 3

    def test_dump(self):
        context = dict(
            c=3
        )

        builtin = '''
          a:
            a1: 1
          b:
          - 1
          - 2
          - %(c)s
        '''

        root = Root(builtin, context)
        dump = root.dumps()
        assert dump == 'a:\n  a1: 1\nb:\n- 1\n- 2\n- 3\n'

