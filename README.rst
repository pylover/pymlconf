pymlconf
========

**pymlconf** (Python YAML Configuration Library) helps to easily manage
and access to your application configurations which was already Written
in `YAML <http://pyyaml.org>`__ language.

It can merge two or more configuration files according their names and
automatically treat file-names as namespaces, or simply merge several
parts of configuration(YAML-string or Python-dict) on arbitrary config
node. for more informations see
`documentations <https://github.com/pylover/pymlconf#documentation>`__.

::

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

Installation
~~~~~~~~~~~~

Latest stable version:

::

    $ pip install pymlconf
    # or
    $ easy_install pymlconf

Development version:

::

    $ pip install git+git@github.com:pylover/pymlconf.git

From source:

::

    $ cd source_dir
    $ python setup.py install

Manually download it from
`pypi <https://pypi.python.org/pypi/pymlconf>`__

Unit-Tests
~~~~~~~~~~

Install nose and change current directory to project's dir:

::

    $ pip install nose  
    $ cd path/to/pymlconf 

Running tests:

::

    $ nosetests
        

Or

::

    $ python setup.py test

Syntax Reference
~~~~~~~~~~~~~~~~

You can find the canonical syntax reference on
`PyYAML <http://pyyaml.org/wiki/PyYAMLDocumentation#YAMLsyntax>`__ site

Documentation
~~~~~~~~~~~~~

-  [pythonhosted.org] (http://pythonhosted.org/pymlconf/)
-  [readthedocs.org] (http://pymlconf.readthedocs.org/en/latest/)

