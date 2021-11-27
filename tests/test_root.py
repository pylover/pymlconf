import pytest
from os import path

from pymlconf import Root


class TestConfigManager:
    def test_constructor(self):
        builtin = '''
          a:
            a1: 1

          b:
          - 1
          - 2
          - 3
        '''

        root = Root(builtin)
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

    def test_loadfile(self):
        here = path.dirname(__file__)
        filename = path.join(here, 'files/sample.yml')
        root = Root()
        root.loadfile(filename)
        assert root.a.b == 2

        with pytest.raises(FileNotFoundError):
            root.loadfile('not/exists')

    def test_dump(self):
        builtin = '''
          a:
            a1: 1
          b:
          - 1
          - 2
          - 3
        '''

        root = Root(builtin)
        dump = root.dumps()
        assert dump == 'a:\n  a1: 1\nb:\n- 1\n- 2\n- 3\n'
