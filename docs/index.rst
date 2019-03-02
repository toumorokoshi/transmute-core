What is transmute-core?
=======================

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
* has a documentation page for all APIs generated this way, via `swagger <http://swagger.io/>`_.

The example above is for flask, but transmute-core has integrations for:

* `aiohttp <https://aiohttp.readthedocs.io/en/stable/>`_
* `flask <http://flask.pocoo.org/>`_
* `tornado <http://www.tornadoweb.org/en/stable/>`_

To learn more, see the :doc:`tutorial`.

License
-------

transmute-core is released under the `MIT license <https://github.com/toumorokoshi/transmute-core/blob/master/LICENSE>`_.

However, transmute-core bundles `swagger-ui
<https://github.com/swagger-api/swagger-ui>`_ with it, which is released under
the Apache2 license.

User's Guide
------------

.. toctree::
    :maxdepth: 2
    :caption: User's Guide

    tutorial
    serialization
    function


.. toctree::
    :maxdepth: 2
    :glob:
    :hidden:
    :caption: Framework Specific Guides

    frameworks/*

.. toctree::
    :maxdepth: 2
    :glob:
    :hidden:
    :caption: Advanced Topics

    advanced/*


API Reference
-------------


.. toctree::
   :maxdepth: 2
   :hidden:
   :caption: API

   api


.. toctree::
   :maxdepth: 2
   :hidden:
   :caption: Changelog

   changelog
