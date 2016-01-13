# -*- coding: utf-8 -*-
"""
Created on Nov 17, 2013

@author: vahid
"""
import unittest
from os import path
from pymlconf.errors import ConfigurationMergeError
from pymlconf import ConfigManager


thisdir = path.join(path.dirname(__file__))


class TestMerge(unittest.TestCase):
    def setUp(self):
        self._builtin = '''
app:
    name: MyApp
    listen:
        sock1:
            addr: 192.168.0.1
            port: 8080
        sock2:
            addr: 127.0.0.1
            port: "89"
logging:
    logfile: /var/log/myapp.log

background: [255, 255, 255]

'''

    def test_overiding_branch(self):
        """
        Testing Branch overriding
        """

        cm = ConfigManager(init_value=self._builtin)

        self.assertEqual(cm.background, [255, 255, 255])

        # testing merge
        additinal_config = """
my_section:
    item1:    hi
app:
    listen:
        sock3:
            addr: 10.8.0.2
            port: 9090
"""
        cm.merge(additinal_config)
        self.assertEqual(cm.app.name, "MyApp")
        self.assertEqual(len(cm.app.listen), 3)
        self.assertEqual(cm.app.listen.sock1.addr, "192.168.0.1")
        self.assertEqual(cm.app.listen.sock1.port, 8080)
        self.assertEqual(cm.app.listen.sock2.addr, "127.0.0.1")
        self.assertEqual(cm.app.listen.sock2.port, '89')
        self.assertEqual(cm.app.listen.sock3.addr, "10.8.0.2")  # Issue 7
        self.assertEqual(cm.app.listen.sock3.port, 9090)  # Issue 7
        self.assertEqual(cm.logging.logfile, "/var/log/myapp.log")

        self.assertEqual(cm.my_section.item1, "hi")

        # testing replace
        additinal_config = """
my_section:
    item1:    hi
app:
    listen: false
"""
        cm.merge(additinal_config)
        self.assertEqual(cm.my_section.item1, "hi")
        self.assertEqual(cm.app.listen, False)  # Issue 7

    def test_issue9(self):
        """
        Test just loading config files: https://github.com/pylover/pymlconf/issues/9
        """
        files = [path.join(thisdir, 'files', 'pytest_sauce.conf')]
        _cm = ConfigManager(files=files)
        self.assertTrue(_cm != None)
        _cm.merge("""
browsers:
    -   browsername: chrome
        platform: linux
        driver: chrome
        """)

    def test_files_with_list_root(self):
        files = [path.join(thisdir, 'conf', 'browsers.yaml')]
        self.assertRaises(ConfigurationMergeError,
                          callableObj=lambda: ConfigManager(files=files))


# Aims to test `ConfigDict` and `ConfigList`


if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
