.. transmute-core documentation master file, created by
   sphinx-quickstart on Fri Apr 15 00:25:27 2016.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

transmute-core
==============

transmute-core removes the boilerplate of writing well-documented, easy to use APIs for Python web services, and easily integrates with any web framework. It takes a function
that looks like this:

.. code-block:: python 

    from transmute_core import annotate
    from transmute_core.frameworks.flask import route

    @route(app, paths='/multiply', tags=['math'])
    def multiply(left: int, right: int) -> int:
        return left * right

Into an API /multiply that:

* validates and serializes objects into the proper object
* has an :doc:`autodocumentation <autodocumentation>` page for all APIs generated this way, via `swagger <http://swagger.io/>`_.

The example above is for flask, but transmute-core has integrations for:

* `aiohttp <https://github.com/toumorokoshi/aiohttp-transmute>`_
* `flask <https://github.com/toumorokoshi/flask-transmute>`_

To learn more, see the 

transmute-core is released under the `MIT license <https://github.com/toumorokoshi/transmute-core/blob/master/LICENSE>`_.

However, transmute-core bundles `swagger-ui
<https://github.com/swagger-api/swagger-ui>`_ with it, which is released under
the Apache2 license.

User's Guide:

.. toctree::
   :maxdepth: 2

   function
   serialization
   autodocumentation
   response
   context
   creating_a_framework
   install


API Reference:


.. toctree::
   :maxdepth: 2

   api


Changelog:

.. toctree::
   :maxdepth: 2

   changelog
