pymlconf
========

**pymlconf** (Python YAML Configuration Library) helps to easily manage
and access to your application configurations which was already Written
in `YAML <http://pyyaml.org>`__ language.

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

    pip install git+git@github.com:pylover/pymlconf.git

From source:

::

    $ cd source_dir
    $ python setup.py install

Syntax Reference
~~~~~~~~~~~~~~~~

You can find the canonical syntax reference on
`PyYAML <http://pyyaml.org/wiki/PyYAMLDocumentation#YAMLsyntax>`__ site
