=====
flask
=====

Gotchas to Note
===============

Flask normally using arrow quotes (<>) to specify variables in the path.
Transmute-core uses the curly brackets ({}) to define path routes instead:

.. code-block:: python

    @route(app, paths='/{foo}')
    def foo_path(foo: str) -> int:
        return 1

Concise Example
===============

.. code-block:: python

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