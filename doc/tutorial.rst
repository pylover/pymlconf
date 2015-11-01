Tutorial
========

Story
-----

Assume we need to provide flexible configuration for a web application.

We have tree configuration levels:
 
 * builtin configurations
 * User configurations
 * Admin configurations


Config files
------------

app/conf/users/sites.mysite.conf::

   name: mysite.com
   owner:
      name: My Name
      phone: My Phone Number
      address: My Address
   
app/conf/admin/root.conf::

   server:
      version: 0.3a
      
   sites:
      admin:
         name: admin.site.com
         owner:
            name: Admin Name
            phone: Admin Phone Number
            address: Admin Address
     
app/conf/admin/server.conf::
   
   host: 0.0.0.0
   port: 80
   
../other_path/../special.conf::

   licence_file: /path/to/file
   log_file: /path/to/file


app/src/builtin_config.py::

   _builtin_config={
      'server':{'name':'Power Server'}
   }

OR::

   _builtin_config="""
   
   server:
      name: Power Server
   
   """
   
Initialize
----------

You can simply merge all config files above with on statement::

   from pymlconf import ConfigManager
   from app.builtin_config import _builtin_config
      
   config_root = ConfigManager(
      _builtin_config,
      ['app/conf/admin','app/conf/users'],
      '../other_path/../special.conf')
      
   # All from app/conf/users/sites.mysite.conf
   print config_root.sites.mysite.name
   print config_root.sites.mysite.owner.name
   print config_root.sites.mysite.owner.address
   print config_root.sites.mysite.owner.phone
   
   # All from app/conf/admin/root.conf
   print config_root.sites.admin.name
   print config_root.sites.admin.owner.name
   print config_root.sites.admin.owner.address
   print config_root.sites.admin.owner.phone
   
   print config_root.server.name       # from _builtin_config
   print config_root.server.version    # from app/conf/admin/root.conf
   print config_root.server.host       # from app/conf/admin/server.conf
   print config_root.server.port       # from app/conf/admin/server.conf
   
   print config_root.licence_file      # from ../other_path/../special.conf
   print config_root.log_file          # from ../other_path/../special.conf





Reserved Keys
-------------

- keys
- can_merge
- copy
- empty
- merge