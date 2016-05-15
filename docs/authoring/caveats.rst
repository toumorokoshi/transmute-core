=======
Caveats
=======

----------------------------------------------------------
Incompatibilities with conventions of the target framework
----------------------------------------------------------

Path parameters
===============

In order for transmute to accurately generate documentation for a
route, it must be known which parameters are extracted from the path.

For most libraries, it is difficult to determine this from the
function signature alone, because the they implement a binding pattern
that only occurs after the function is defined. e.g. Tornado's:

.. code-block:: python

    Application([
        // the path is bound to the handler
        // AFTER the handler itself is defined.
        ("/my_path/{path}", handler)
    ])

or aiohttp:

.. code-block:: python

    app.router.add_route("GET", "/api/v1/login", login)


As such, it is often required to combine the binding and the function
generator into a single decorator:

.. code-block:: python

   # tornado example
   Application([
       transmute.to_route_tuple("/my_path/{path}", raw_func)
   ])


.. code-block:: python

   # aiohttp
   transmute.add_route(app.router, "/api/v1/login", login_raw)


When desiging the API, it is recommended to find the least invasive
approach to accomplishing the binding.

---------------------------
Path Templating and Swagger
---------------------------

The choice of the path definition language is language-specific: e.g.
flask uses <> to identify a variable part of the path.

Swagger specifications expects
