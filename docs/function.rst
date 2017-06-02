======================================
Writing transmute-compatible functions
======================================

.. _functions:

.. note:: this section is broadly applicable to all transmute frameworks.

Functions are converted to APIs by using an intermediary TransmuteFunction object.

A transmute function is identical to a standard Python function, with the
addition of a few details:

------------------------------------------------------------------
Add function annotations for input type validation / documentation
------------------------------------------------------------------

if type validation and complete swagger documentation is desired,
arguments should be annotated with types.  For Python 3, `function
annotations <https://www.python.org/dev/peps/pep-3107/>`_ are used.

For Python 2, transmute provides an annotate decorator:

.. code-block:: python

   import transmute_core

   # the python 3 way
   def add(left: int, right: int) -> int:
        return left + right

   # the python 2 way
   @transmute_core.annotate({"left": int, "right": int, "return": int})
   def add(left, right):
       return left + right


By default, primitive types and `schematics <http://schematics.readthedocs.org/en/latest/>`_ models are
accepted. See :ref:`serialization <serialization>` for more information.

--------------------------------------------------
Use transmute_core.describe to customize behaviour
--------------------------------------------------

Not every aspect of an api can be extracted from the function
signature: often additional metadata is required. Transmute provides the "describe" decorator
to specify those attributes.

.. code-block:: python

    import transmute_core  # these are usually also imparted into the
    # top level module of the transmute

    @transmute_core.describe(
        methods=["PUT", "POST"],  # the methods that the function is for
        # the source of the arguments are usually inferred from the method type, but can
        # be specified explicitly
        query_parameters=["blockRequest"],
        body_parameters=["name"]
        header_parameters=["authtoken"]
        path_parameters=["username"]
    )
    def create_record(name: str, blockRequest: bool, authtoken: str, username: str) -> bool:
        if block_request:
            db.insert_record(name)
        else:
            db.async_insert_record(name)
        return True



----------
Exceptions
----------

By default, transmute functions only catch exceptions which extend
:class:`transmute_core.APIException`, which results in an http response
with a non-200 status code. (400 by default):


.. code-block:: python

    from transmute_core import APIException

    def my_api() -> int:
        if not retrieve_from_database():
            raise APIException(code=404)

However, many transmute frameworks allow the catching of additional
exceptions, and converting them to an error response.


-----------------------------------------------------
Query parameter arguments vs post parameter arguments
-----------------------------------------------------

The convention in transmute is to have the method dictate the source of the
argument:

* GET uses query parameters
* all other methods extract parameters from the body

This behaviour can be overridden with :data:`transmute_core.decorators.describe`.

-------------------
Additional Examples
-------------------

Optional Values
===============

transmute libraries support optional values by providing them as keyword arguments:

.. code-block:: python

    # count and page will be optional with default values,
    # but query will be required.
    def add(count: int=100, page: int=0, query: str) -> [str]:
        return db.query(query=query, page=page, count=count)

Custom Response Code
====================

In the case where it desirable to override the default response code, the
response_code parameter can be used:

.. code-block:: python

    @describe(success_code=201)
    def create() -> bool:
        return True

Use a single schema for the body parameter
==========================================

It's often desired to represent the body parameter as a single
argument. That can be done using a string for body_parameters describe:

.. code-block:: python

    @describe(body_parameters="body", methods="POST"):
    def submit_data(body: int) -> bool:
        return True


Multiple Response Types
=======================

To allow multiple response types, there is a combination of types that
can be used:

.. code-block:: python

    from transmute_core import Response

    @describe(paths="/api/v1/create_if_authorized/",
              response_types={
                  401: {"type": str, "description": "unauthorized"},
                  201: {"type": bool}
              })
    @annotate({"username": str})
    def create_if_authorized(username):
        if username != "im the boss":
            return Response("this is unauthorized!", 401)
        else:
            return Response(True, 201)

note that adding these will remove the documentation and type honoring
for the default success result: it is assumed you will document all non-400
responses in the response_types dict yourself.


Headers in a Response
=====================

Headers within a response also require defining a custom response type:

.. code-block:: python

    from transmute_core import Response

    @describe(paths="/api/v1/create_if_authorized/",
              response_types={
                  200: {"type": str, "description": "success",
                        "headers": {
                            "location": {
                                "description": "url to the location",
                                "type": str
                            }
                        }
                  },
              })
    def return_url():
        return Response("success!", headers={
            "location": "http://foo"
        })
