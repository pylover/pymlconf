import unittest

from pymlconf import Root, Mergable


class MergeTestCase(unittest.TestCase):

    def test_merge_empty_object(self):
        root = Root()
        root.merge('')
        self.assertEqual(0, len(root.keys()))

    def test_merge_errors(self):
        root = Root()
        with self.assertRaises(TypeError):
            root.merge(None)

    def test_merge_deep_object(self):
        root = Root()
        root.merge('''
          a:
            b:
              c: 3
        ''')

        self.assertEqual(3, root.a.b.c)
        root.merge('''
          d:
            e: 1
        ''')

        self.assertIsInstance(root.d, Mergable)

        root.d.merge(root.a)
        self.assertEqual(3, root.d.b.c)

        root.a.b = 2
        self.assertEqual(2, root.a.b)
        self.assertEqual(3, root.d.b.c)

    def test_merge_list(self):
        root = Root()
        root.merge('''
          a:
            b:
             - 1
             - 2
          c: []
        ''')

        self.assertEqual([1, 2], root.a.b)

        root.c.merge(root.a.b.copy())
        root.a.b.append(3)
        self.assertEqual([1, 2, 3], root.a.b)
        self.assertEqual([1, 2], root.c)


if __name__ == '__main__':  # pragma: no cover
    unittest.main()

