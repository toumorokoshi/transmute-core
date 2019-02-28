=====
Functions and Annotations
=====

transmute-core infers a lot of data from the function metadata, but it's often necessary to express more complex scenarios.

This page discusses some details.

Argument Inference
=====

The convention in transmute is to have the method dictate the source of the
argument:

* GET uses query parameters
* all other methods extract parameters from the body

This behaviour can be overridden with transmute_core.describe.

use transmute_core.describe to customize behaviour
=====

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
        path_parameters=["username"],
        parameter_descriptions={
          "blockRequest": "if true, the request will be blocked.",
          "name": "the name of the db record to insert."
        }
    )
    def create_record(name: str, blockRequest: bool, authtoken: str, username: str) -> bool:
        if block_request:
            db.insert_record(name)
        else:
            db.async_insert_record(name)
        return True

Exceptions
=====

By default, transmute functions only catch exceptions which extend
transmute_core.APIException. When caught, the response is an http response with a non-200 status code. (400 by default):


.. code-block:: python

    from transmute_core import APIException

    def my_api() -> int:
        if not retrieve_from_database():
            raise APIException(code=404)

Many transmute frameworks allow the catching of additional
exceptions, and converting them to an error response. See the framework specific guides for more details.


Additional Examples
=====


Optional Values
-----

transmute libraries support optional values by providing them as keyword arguments:

.. code-block:: python

    # count and page will be optional with default values,
    # but query will be required.
    def add(count: int=100, page: int=0, query: str) -> List[str]:
        return db.query(query=query, page=page, count=count)

Custom Response Code
-----

In the case where it desirable to override the default response code, the
response_code parameter can be used:

.. code-block:: python

    @describe(success_code=201)
    def create() -> bool:
        return True

Use a single schema for the body parameter
-----

It's often desired to represent the body parameter as a single
argument. That can be done using a string for body_parameters describe:

.. code-block:: python

    @describe(body_parameters="body", methods="POST"):
    def submit_data(body: int) -> bool:
        return True


Multiple Response Types
-----

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
for the default success result: it is assumed you will document all non-400 responses in the response_types dict yourself.


Headers in a Response
-----

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

