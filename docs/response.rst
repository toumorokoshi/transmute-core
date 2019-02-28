========
Response
========

--------------
Response Shape
--------------

The response shape describes what sort of object is returned back by the HTTP
response in cases of success.

Simple Shape
============

As of transmute-core 0.4.0, the default response shape is simply the
object itself, serialized to the primitive content type. e.g.

.. code-block:: python

    from transmute_core import annotate
    from schematics.models import Model
    from schematics.types import StringType, IntType

    class MyModel(Model):
        foo = StringType()
        bar = IntType()

    @annotate("return": MyModel)
    def return_mymodel():
        return MyModel({
            "foo": "foo",
            "bar": 3
        })

Would return the response

.. code-block:: json

    {
        "foo": "foo",
        "bar": 3
    }

Complex Shape
=============

Another common return shape is a nested object, contained inside a layer
with details about the response:

.. code-block:: json

    {
        "code": 200,
        "success": true,
        "result": {
            "foo": "foo",
            "bar": 3
        }
    }

This can be enabled by modifying the default context, or passing a
custom one into your function:

.. code-block:: python

    from transmute_core import (
        default_context, ResponseShapeComplex,
        TransmuteContext
    )

    # modifying the global context, which should be done
    # before any transmute functions are called.
    default_context.response_shape = ResponseShapeComplex

    # passing in a custom context
    context = TransmuteContext(response_shape=ResponseShapeComplex)

    transmute_route(app, fn, context=context)

Custom Shapes
=============

Any class or object which implements :class:`transmute_core.response_shape.ResponseShape`
can be used as an argument to response_shape.
