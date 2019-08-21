Tutorial
========


Install
-------


.. code-block:: bash

   pip install pymlconf


Usage
-----

The entry point of the library is the :class:`.Root` class. But a proxy: 
:class:`.DeferredRoot` is also provided to let users import root object 
before initialization.

.. code-block:: python

   from pymlconf import DeferredRoot

   settings = DeferredRoot()


Import ``settings`` everywhere in your application's source code.

Then you may initialize the ``settings`` object when your data is ready:

.. code-block:: python

   context = {
       'here': 'path/to/here'
   }

   builtins = '''
     a: %(here)s
    '''

   settings.initialzie(builtins, context)
   print(settings.a)


Loading YAML files
-------------------

You can load and merge your configuration file(s) using
:meth:`.Root.load_file`.


.. code-block:: python

   settings.loadfile(filename)

