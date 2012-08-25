'''
Created on Jul 25, 2011

@author: vahid
'''

import os
import unittest
from pymlconf import ConfigDict, ConfigList, ConfigManager, ConfigNode

instance_dir = os.path.abspath(os.path.dirname(__file__))
conf_dir = os.path.join(instance_dir, 'conf')
class TestConfigManager(unittest.TestCase):
    
    def setUp(self):
        self.builtin_config = {
            'version'   : 2.5,
            'general'   : ConfigDict({'name':'albatross'}),
            'domains'   : ConfigDict({'coldon_ir':ConfigDict(), 'fangtooth_ir':ConfigDict({'name':'fangtooth'})}),
            'data'      : {'url': 'some uri'} # without ConfigDict
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
        
    def test_import(self):
        _cd = ConfigDict
        _cl = ConfigList
        _cn = ConfigNode
                
        
if __name__ == '__main__':
    unittest.main()
