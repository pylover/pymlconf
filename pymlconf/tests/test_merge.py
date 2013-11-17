# -*- coding: utf-8 -*-
'''
Created on Nov 17, 2013

@author: vahid
'''
import unittest

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
logging:
    logfile: /var/log/myapp.log
'''


    def test_overiding_branch(self):
        """
        Testing Branch overriding
        """
        
        cm = ConfigManager(init_value=self._builtin)
        
        additinal_config="""
my_section:
    item1:    hi
app:
    listen: false
"""
        cm.merge(additinal_config)
        self.assertEqual(cm.my_section.item1, "hi")
#        self.assertEqual(cm.app.listen, False) #Issue 7
        
        
        
        
#Aims to test `ConfigDict` and `ConfigList`        


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()