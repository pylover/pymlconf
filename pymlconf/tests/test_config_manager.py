
import os
import unittest
if __name__ == '__main__' and not __package__:
    from os import path,sys
    sys.path.append(path.abspath(path.join(path.dirname(__file__),'..','..')))
    import pymlconf
    __package__ = 'pymlconf.tests'


from ..__init__ import ConfigDict, ConfigManager

this_dir = os.path.abspath(os.path.dirname(__file__))
conf_dir = os.path.join(this_dir, 'conf')

class TestConfigManager(unittest.TestCase):

    def setUp(self):
        self.builtin_config = {
            'version': 2.5,
            'general': {'name': 'albatross'},
            'domains': ConfigDict({'coldon_ir': ConfigDict(), 'fangtooth_ir': ConfigDict({'name': 'fangtooth'})}),
            'data': {'url': 'some uri'}  # without ConfigDict
        }

    def test_builtins(self):
        cm = ConfigManager(init_value=self.builtin_config)
        cm.version = 2.6
        self.assertEqual(cm.version, 2.6)
        self.assertEqual(cm.general.name, self.builtin_config['general']['name'])
        self.assertIsInstance(cm.domains['coldon_ir'], ConfigDict)
        self.assertEqual(cm.data.url, 'some uri')

    def test_files(self):

        files = [os.path.join(conf_dir, '../files', 'c111.conf')]
        cm = ConfigManager(init_value=self.builtin_config, dirs=[conf_dir], files=files)

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

    def test_dirs(self):
        dirs = [conf_dir]
        cm = ConfigManager(init_value=self.builtin_config, dirs=dirs)

        # root.conf
        self.assertEqual(cm.version, 2.5)
        self.assertEqual(cm.domains['coldon_ir'].name, 'coldon')
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

        # builtins
        self.assertEqual(cm.data.url, 'some uri')
