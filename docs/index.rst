.. transmute-core documentation master file, created by
   sphinx-quickstart on Fri Apr 15 00:25:27 2016.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

transmute-core
==============

transmute-core is a set of web framework agnostic APIs that allow developers to quickly generate http apis
with schema validation and documentation.

specifically, transmute-core provides:

* declarative generation of http handler interfaces by parsing :ref:`python functions <functions>`.
* validation and serialization to and from a variety of content types (e.g. json or yaml).
* validation and serialization to and from native python objects which use `schematics <http://schematics.readthedocs.org/en/latest/>`_.
* :doc:`autodocumentation <autodocumentation>` of all handlers generated this way, via `swagger <http://swagger.io/>`_.

To use this functionality, it's recommended to build or use a
framework-specific wrapper library, to handle a more fluid integration.

An example in flask looks like:

.. code-block:: python

    import flask_transmute
    from flask import Flask

    app = Flask(__name__)


    # api GET method, path = /multiply
    # take query arguments left and right which are integers, return an
    # integer.
    @flask_transmute.route(app, paths='/multiply')
    @flask_transmute.annotate({"left": int, "right": int, "return": int})
    def multiply(left, right):
        return left * right

    # finally, you can add a swagger json and a documentation page by:
    flask_transmute.add_swagger(app, "/swagger.json", "/swagger")

    app.run()

transmute-core is released under the `MIT license <https://github.com/toumorokoshi/transmute-core/blob/master/LICENSE>`_.


Implementations exist for:

* `aiohttp <https://github.com/toumorokoshi/aiohttp-transmute>`_
* `flask <https://github.com/toumorokoshi/flask-transmute>`_
* `sanic <http://sanic-transmute.readthedocs.io/en/latest/>`_

If you are interested in creating a transmute library for your
preferred web framework, please read :doc:`creating_a_framework`.
If you are interested in having it appear on this page,
please send a PR against the core project.

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
