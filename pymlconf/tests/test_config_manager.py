import re
import unittest
from os import path

from pymlconf import MergableDict, MergableList


here = path.abspath(path.dirname(__file__))
data_directory = path.abspath(path.join(this_dir, 'conf'))


class TestConfigManager(unittest.TestCase):
    def setUp(self):
        self.initial_config = {
            'version': 2.5,
            'general': {'name': 'albatross'},
            'domains': ConfigDict({
                'coldon_ir': ConfigDict(),
                'fangtooth_ir': ConfigDict({'name': 'fangtooth'})
            }),
            'data': {'url': 'some uri'}  # without ConfigDict
        }

    def test_builtins(self):
        a_date = '2014/12/01'

        builtin = """
        builtin:
          value1: built-in config value
        """

        cm = ConfigManager(builtin=builtin, init_value=self.initial_config, context=dict(date=a_date))
        self.assertEqual(cm.builtin.value1, 'built-in config value')
        cm.merge("""
            a_date: %(date)s
        """)
        self.assertEqual(cm.version, 2.5)
        cm.version = 2.6
        self.assertEqual(cm.version, 2.6)
        self.assertEqual(cm.a_date, a_date)
        self.assertEqual(cm.general.name, self.initial_config['general']['name'])
        self.assertIsInstance(cm.domains['coldon_ir'], ConfigDict)
        self.assertEqual(cm.data.url, 'some uri')

    def test_files(self):

        # noinspection PyUnresolvedReferences
        files = [os.path.join(conf_dir, '../files', 'c111.conf'),
                 os.path.join(conf_dir, '../files', 'something-that-not-exists.conf')]
        cm = ConfigManager(init_value=self.initial_config, dirs=[conf_dir], files=files)

        # root.conf
        self.assertEqual(cm.version, 2.5)
        self.assertEqual(cm.domains.coldon_ir.name, 'coldon')
        self.assertEqual(cm.general.tcp_port, 5671)

        # general.conf
        self.assertEqual(cm.general.name, 'Vahid')
        self.assertEqual(cm.domains['fangtooth_ir'].name, 'Fangtooth2')

        # domains_coldon.ir.conf
        self.assertEqual(cm.domains['coldon_ir'].path, '/home/local/coldon')

        # domains_dobisel.com.conf
        self.assertEqual(cm.domains['dobisel_com'].path, '/home/local/dobisel')
        self.assertEqual(cm.domains['dobisel_com'].name, 'dobisel')
        self.assertEqual(cm.domains['dobisel_com'].applications.app1.name, 'app1')
        self.assertEqual(cm.domains['dobisel_com'].applications.app2.users.vahid.fullname, 'Vahid Mardani')
        self.assertEqual(cm.domains['dobisel_com'].applications.app2.users.vahid.password, 'himopolxx')
        self.assertEqual(cm.baghali, 2)
        # builtins
        self.assertEqual(cm.data.url, 'some uri')


if __name__ == '__main__':  # pragma: no cover
    unittest.main()
