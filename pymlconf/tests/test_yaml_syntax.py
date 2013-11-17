# -*- coding: utf-8 -*-
'''
Created on Nov 17, 2013

@author: vahid
'''
import unittest
if __name__ == '__main__' and not __package__:
    from os import path,sys
    sys.path.append(path.abspath(path.join(path.dirname(__file__),'..','..')))
    import pymlconf
    __package__ = 'pymlconf.tests'
    
from ..__init__ import ConfigManager


class Test(unittest.TestCase):

    def setUp(self):
        self._builtin='''
app:
    name: MyApp
    listen:
        sock1:
            addr: 192.168.0.1
            port: 8080
        sock2:
            addr: 127.0.0.1
            port: "89"
    languages:
        - english
        - {language: persian, country: iran}
        
logging:
    logfile: /var/log/myapp.log
'''


    def test_simple_syntax(self):
        """
        Testing simple Yaml syntax
        """
        
        cm = ConfigManager(init_value=self._builtin)
        self.assertEqual(cm.app.name, "MyApp")
        self.assertEqual(len(cm.app.listen), 2)
        self.assertEqual(cm.app.listen.sock1.addr, "192.168.0.1")
        self.assertEqual(cm.app.listen.sock1.port, 8080)
        self.assertEqual(cm.app.listen.sock2.addr, "127.0.0.1")
        self.assertEqual(cm.app.listen.sock2.port, '89')
        self.assertEqual(cm.logging.logfile, "/var/log/myapp.log")
        
        self.assertEqual(len(cm.app.languages),2)
        self.assertEqual(cm.app.languages[0],'english')
        self.assertEqual(cm.app.languages[1].language,'persian')
        self.assertEqual(cm.app.languages[1].country,'iran')
        
#Aims to test `ConfigDict` and `ConfigList`        


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()