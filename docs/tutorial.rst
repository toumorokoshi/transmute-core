===============
Getting Started
===============

This guide explains how to get the most out of transmute. These instructions have been written with flask in mind, but they apply to most frameworks with some minor tweaks.

For details that pertain to a specific framework, see framework support.

From a high level, the steps are:

1. authoring a function that you would like to be an API
2. annotating the function with data needed to describe how it should be exposed (method, path)
3. adding a route that exposes the swagger documentation page, displaying all transmute routes created

1. Authoring a Function To Be Transmuted
----------------------------------------

transmute-core is very flexible with regards to what sort of functions can be converted into APIs. The more best practices followed, the better.

Here's an ideal example:

.. code-block:: python

    def multiply(left: int, right: int) -> int:
        """
        multiply two values together.
        """
        return left * right

transmute will extract relevant metadata about the function and use that to define certain attributes when creating the API. In the example above:

* multiply will allow two arguments: left and right, which are both integers
* the api will return back an integer
* the description of the api in documentation is "multiply two values together"

More complex objects can be used. See [serialization](serialization.md).

----------------------------
Annotating Types in Python 2
----------------------------

The example above uses type annotations, which are only present in Python 3.4 and above. If you are using an older version, transmute-core provides the "annotate" decorator to provide the same data.

.. code-block:: python

    from transmute_core import annotate

    @annotate({"left": int, "right": int, "return": int})
    def multiply(left, right):
        """
        multiply two values together.
        """
        return left * right

2. Annotating a Function
------------------------

This provides some of the data, but there is some missing information to fully define an API:

* the route that the API should be mounted to
* the method(s) that the API should respond to 
* additional configuration, like where parameters should be found.

We can add that information with the describe function from transmute_core:

.. code-block:: python

    from transmute_core import annotate, describe

    @describe(paths='/multiply', methods=["POST"])
    def multiply(left: int, right: int) -> int:
        """
        multiply two values together.
        """
        return left * right

This specifies:

* the api should be mounted to the path /multiply
* multiply will respond to the POST method
* since the method is POST, all arguments should be passed into the body

To attach the result to a flask application, transmute_core.frameworks.flask provides a route() function.

.. code-block:: python

    from transmute_core.frameworks.flask import route
    from flask import Flask

    app = Flask(__name__)

    @route(app)
    @describe(paths='/multiply', methods=["POST"])
    def multiply(left: int, right: int) -> int:
        """
        multiply two values together.
        """
        return left * right

As a shorthand, you can also pass configuration parameters into route as you would describe:


.. code-block:: python

    from transmute_core.frameworks.flask import route
    from flask import Flask

    app = Flask(__name__)

    @route(app, paths='/multiply', methods=["POST"])
    def multiply(left: int, right: int) -> int:
        """
        multiply two values together.
        """
        return left * right

    if __name__ == "__main__":
        app.run(debug=True)

At this point, you can start the server, and you can send it requests! Try it out::

    $ curl http://localhost:8000/multiply --data='{"left": 10, "right": 20}'

But what about an easy way to view what APIs are available?

3. Adding Swagger Documentation to the App
------------------------------------------

As part of the route creation and mounting process, transmute will also add metadata that's easily discoverable.
That metadata can be exposed as a swagger json payload. In addition, transmute-core bundles the swagger UI so you can 
view it easily as a part of your application.

This is wrapped up as a single convenience method, provided per framework. For flask, it's transmute_core.frameworks.add_swagger:

.. code-block:: python

    from transmute_core.frameworks.flask import add_swagger

    # note: this must be executed only after all APIs are mounted.
    add_swagger(app, "/swagger.json", "/api/")

This mounts the swagger json payload to /swagger.json, and provides a UI to view that at /api/.

At the end of the day, you can get a well documented API, and provide documentation, with roughly 4 lines from transmute_core.


.. code-block:: python

    from transmute_core.frameworks.flask import route, add_swagger
    from flask import Flask

    app = Flask(__name__)

    @route(app, paths='/multiply', methods=["POST"])
    def multiply(left: int, right: int) -> int:
        """
        multiply two values together.
        """
        return left * right

    add_swagger(app, "/swagger.json", "/api/")

    if __name__ == "__main__":
    app.run(debug=True)

Congrats! You have an application up.

4. What's Next?
---------------

You now have everything you need to get started with transmute! If you're
interested in more complex objects in your apis, take a look at :doc:`serialization`.

If you're looking for more complex use cases for the APIs such as specifying 
how parameters should be passed in, check out :doc:`function`.
