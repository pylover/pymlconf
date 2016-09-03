pymlconf
========

.. image:: http://img.shields.io/pypi/v/pymlconf.svg
     :target: https://pypi.python.org/pypi/pymlconf

.. image:: https://requires.io/github/pylover/pymlconf/requirements.svg?branch=master
     :target: https://requires.io/github/pylover/pymlconf/requirements/?branch=master
     :alt: Requirements Status

.. image:: https://travis-ci.org/pylover/pymlconf.svg?branch=master
     :target: https://travis-ci.org/pylover/pymlconf

.. image:: https://coveralls.io/repos/github/pylover/pymlconf/badge.svg?branch=master
     :target: https://coveralls.io/github/pylover/pymlconf?branch=master

.. image:: https://img.shields.io/badge/license-GPLv3-brightgreen.svg
     :target: https://github.com/pylover/pymlconf/blob/master/LICENSE


Jump To:
^^^^^^^^

 * `Documentation <http://pymlconf.dobisel.com>`_
 * `Python package index <https://pypi.python.org/pypi/pymlconf>`_
 * `Source on github <https://github.com/pylover/pymlconf>`_
 * `Downloads <https://pypi.python.org/pypi/pymlconf#downloads>`_


About
^^^^^

**pymlconf** (Python YAML Configuration Library) helps to easily manage
and access to your application configurations which was already Written
in `YAML <http://pyyaml.org>`__ language.

It can merge two or more configuration files according their names and
automatically treat file-names as namespaces, or simply merge several
parts of configuration(YAML-string or Python-dict) on arbitrary config
node. for more informations see
`documentations <https://github.com/pylover/pymlconf#documentation>`__.

Config file

::

    # filename: config.yaml
    app:
        root_dir: %(here)s

Python code:

::

    # filename: config.py
    from pymlconf import ConfigManager

    config_str='''
    app:
        name: MyApp
        listen:
            sock1:
                addr: %(hostname)s
                port: %(port)s
        languages:
            - english
            - {language: persian, country: iran}
            
    logfile: /var/log/myapp.log
    '''

    cfg = ConfigManager(init_value=config_str, context=dict(hostname='192.168.0.1', port=8080))
    cfg.load_files('path/to/config.yaml')

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

Deferred(Proxied)
~~~~~~~~~~~~~~~~~

::

    # module configuration.py
    from pymlconf import DeferredConfigManager
    settings = DeferredConfigManager()

    # another_module.py
    from configuration import settings
    def serve_request():
        return settings.message

    # in application startup
    from configuration import settings
    settings.load(
        # the signature is the same as the `ConfigManager.__init__`
    )

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

Change Log
~~~~~~~~~~

-  [0.5.9] ci
-  [0.5.1] Encoding option for files
-  [0.4.0] Adding DeferredConfigManager
