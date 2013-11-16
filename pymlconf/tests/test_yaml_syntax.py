# -*- coding: utf-8 -*-
'''
Created on Nov 17, 2013

@author: vahid
'''
import unittest

from ..__init__ import ConfigManager


class Test(unittest.TestCase):

    def test_simple_syntax(self):
        """
        Testing simple Yaml syntax
        """
        
        _builtin='''
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
'''        
        cm = ConfigManager(init_value=_builtin)
        self.assertEqual(cm.app.name, "MyApp")
        self.assertEqual(len(cm.app.listen), 2)
        self.assertEqual(cm.app.listen.sock1.addr, "192.168.0.1")
        self.assertEqual(cm.app.listen.sock1.port, 8080)
        self.assertEqual(cm.app.listen.sock2.addr, "127.0.0.1")
        self.assertEqual(cm.app.listen.sock2.port, '89')
        self.assertEqual(cm.logging.logfile, "/var/log/myapp.log")
        
        
        
#Aims to test `ConfigDict` and `ConfigList`        


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()