=============
API Reference
=============

----------------
TransmuteContext
----------------

.. autoclass:: transmute_core.context.TransmuteContext
    :members:

----------
Decorators
----------

.. automodule:: transmute_core.decorators
    :members:


--------------------
Object Serialization
--------------------


.. autoclass:: transmute_core.object_serializers.ObjectSerializer
    :members:

.. autoclass:: transmute_core.object_serializers.SchematicsSerializer
    :members:

-------------------------
ContentType Serialization
-------------------------

.. autoclass:: transmute_core.contenttype_serializers.ContentTypeSerializer
    :members:

.. autoclass:: transmute_core.contenttype_serializers.SerializerSet
    :members:

.. autoclass:: transmute_core.contenttype_serializers.JsonSerializer
    :members:

.. autoclass:: transmute_core.contenttype_serializers.YamlSerializer
    :members:

-------
Swagger
-------

.. automodule:: transmute_core.swagger
    :members:

-----------------
TransmuteFunction
-----------------

.. warning:: transmute framework authors should not need to use
             attributes in TransmuteFunction directly.  see
             :doc:`authoring_a_toolbox`


.. automodule:: transmute_core.function.attributes
    :members:

.. automodule:: transmute_core.function.transmute_function
    :members:

.. automodule:: transmute_core.function.signature
    :members:

.. automodule:: transmute_core.function.parameters
    :members:
