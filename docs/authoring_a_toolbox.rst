===================
Authoring a Toolbox
===================

--------
Overview
--------

A transmute library should provide at a minimum the following functionality:

1. a way to convert a transmute_function to a handler for your framework of choice.
2. a way to register a transmute function to the application object
3. a way to generate a swagger.json from an application object

Reference implementations exist at:

* https://github.com/toumorokoshi/aiohttp-transmute
* https://github.com/toumorokoshi/tornado-transmute

.. important:

   transmute-core is deliberately minimal on integration with a framework (such as using
   route decorators a la Flask, or creating handler classes like Tornado). It's recommended
   to implement apis that work well when used with the standard route generation method.

--------
Tutorial
--------

For the tutorial, we will write a transmute library for `Bottle <http://bottlepy.org/>`_.


1. Convert a function to a handler with TransmuteFunction
=========================================================

Bottle's routing uses decorators, and the transmute framework should
go hand in hand with existing routing mechanisms. We could use python decorators
to achieve minimal intrusion:

.. code-block:: python

    import bottle_transmute
    from bottle import route

    @bottle_transmute.to_route("/hello/<name>")
    def hello(name: str) -> str:
        return "hello, " + name


Our to_route function could look something like:

.. code-block:: python

    import bottle
    from transmute_core import (TransmuteFunction, default_context)
    from .handler import create_handler

    # our decorator should take additional parameters, to allow
    # for customization such as custom exceptions.
    #
    # context refers to the TransmuteContext, which
    # allows customization of serializers for both types (the return object)
    # and for content types (e.g. yaml, json)
    def route(path, context=default_context, **options):
        transmute_func = Transmute_func(fn, **options)
        handler = create_handler_for_bottle(transmute_func)
        # we annotate the route with bottle.route so
        # bottle gets it.
        return bottle.route(path, handler)



The two main points are:


1. use :class:`transmute_core.function.TransmuteFunc` to get a transmute_func backh
   the original function annotated with metadata that make generating a route from it easier.
2. author a create_handler_for_bottle function that receive a transmute function, and returns
   back a handler compatible with bottle (or whatever framework of choice)
3. copy how bottle.route works: a decorator which adds the route to the server.

.. tip::

   The route function should take an arbitrary set of keywords. If transmute_core
   allows additional configuration in the future, allowing arbitrary keyword parameters
   allows your library to take advantage of those configuration immediately.

   Hard-coding what to_route accepts would require a code change of
   your library every time TransmuteFunction takes new parameters.


The api reference for :class:`transmute_core.function.TransmuteFunc` has more information,
but TransmuteFunc helps extract configuration such as:

* description
* functions
* return type
* supported http method
* swagger definition

Next comes authoring the create_handler function. For bottle, that
looks something like:

.. code-block:: python

    from functools import wraps
    from transmute_core import APIException
    from bottle import request, response

    def create_handler_for_bottle(transmute_func, context):
        extract_params_func = _get_param_extractor(transmute_func, context)

        @wraps(transmute_func.raw_func)
        def handler(*args, **kwargs):
            args, kwargs = extract_params_func(request, *args, **kwargs)
            try:
                transmute_func.raw_func(*args, **kwargs)
            except APIException as e:
                output = {
                    "result": str(e),
                    "success": False,
                    "code": e.code
                }
            except Exception as e:
                # we reraise the exception, if it's not amount those expected
                # by the API.
                if not isinstance(e, transmute_func.error_exceptions):
                    raise
                output = {
                    "result": str(e),
                    "success": False,
                    "code": e.code
                }
            try:
                body = context.contenttype_serializers.to_type(
                    request.content_type, output
                )
            except NoSerializerFound:
                body = context.contenttype_serializers.to_type("json", output)
            response.status = output["code"]
            response.set_header("Content-Type", request.content_type


Once completed, you will need to build some functions to extract the
parameters to your function. It is usually split into two: one for GET (query parameters),
and one for all other functions (body parameters)
