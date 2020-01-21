import pytest

from pymlconf import Root, Mergable


class TestMerge:

    def test_merge_empty_object(self):
        root = Root()
        root.merge('')
        assert len(root.keys()) == 0

    def test_merge_errors(self):
        root = Root()
        with pytest.raises(TypeError):
            root.merge(None)

    def test_merge_deep_object(self):
        root = Root()
        root.merge('''
          a:
            b:
              c: 3
        ''')

        assert root.a.b.c == 3
        root.merge('''
          d:
            e: 1
        ''')

        assert isinstance(root.d, Mergable)

        root.d.merge(root.a)
        assert root.d.b.c == 3

        root.a.b = 2
        assert root.a.b == 2
        assert root.d.b.c == 3

    def test_merge_list(self):
        root = Root()
        root.merge('''
          a:
            b:
             - 1
             - 2
          c: []
        ''')

        assert root.a.b == [1, 2]

        root.c.merge(root.a.b.copy())
        root.a.b.append(3)
        assert root.a.b == [1, 2, 3]
        assert root.c == [1, 2]

