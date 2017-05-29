================
TransmuteContext
================

.. _transmute-context:

To enable rapidly generating apis, transmute-core has embedded several
defaults and decisions about technology choices (such as Schematics for schema validation).

The :class:`TransmuteContext <transmute_core.TransmuteContext>` allows customizing this behaviour. Transmute
frameworks should allow one to provide and specify their own context by passing it as a keyword argument
during a function call:

.. code:: python

    from flask_transmute import add_route

    add_route(app, fn, context=my_custom_context)

It is also possible to modify transmute_core.default_context: this is
the context that is referenced by all transmute functions by default.
