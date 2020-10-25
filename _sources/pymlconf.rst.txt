API Reference
=============

.. module:: pymlconf

.. autoclass:: Mergable
    
   .. automethod:: canmerge
   .. automethod:: dump
   .. automethod:: copy
   .. automethod:: make_mergable_if_possible
   .. automethod:: merge


.. autoclass:: MergableList
   :show-inheritance:

.. autoclass:: MergableDict
   :show-inheritance:

.. autoclass:: ConfigurationNamespace
   :show-inheritance:

.. autoclass:: Root
   :show-inheritance:
   
   .. automethod:: dumps
   .. automethod:: loadfile

.. autoclass:: DeferredRoot
   :show-inheritance:

   .. automethod:: initialize

.. autoclass:: ConfigurationError
   :show-inheritance:

.. autoclass:: ConfigurationAlreadyInitializedError
   :show-inheritance:

.. autoclass:: ConfigurationNotInitializedError
   :show-inheritance:

