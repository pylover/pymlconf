# -*- coding: utf-8 -*-
'''
Created on:    Nov 17, 2013
@author:        vahid
'''

from pymlconf import ConfigManager

config_str='''
app:
    name: MyApp
    listen:
        sock1:
            addr: 192.168.0.1
            port: 8080
    languages:
        - english
        - {language: persian, country: iran}
        
logfile: /var/log/myapp.log
'''

cfg = ConfigManager(init_value=config_str)

print cfg.app.name
print cfg.app.listen.sock1.addr
print cfg.app.languages[0]
print cfg.app.languages[1].country
print cfg.logfile

# --------- Prints:
# MyApp
# 192.168.0.1
# english
# iran
# /var/log/myapp.log


