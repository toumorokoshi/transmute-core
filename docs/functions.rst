======================================
Writing Transmute-compatible Functions
======================================

Transmute functions are converted to APIs by reading various details:

A transmute function is identical to a standard Python function, with the
additional of a few details:

----------------------------------
Use a decorator on non-GET methods
----------------------------------

By default, functions with no decorators will be converted to an HTTP GET method.
Other request types should be annotated with a PUT, DELETE, or POST as appopriate.

.. code-block:: python

    import transmute_core  # these are usually also imparted into the
    # top level module of the transmute

    @transmute_core.PUT
    def create_record(name: str):
        db.insert_record(name)


------------------------------------------------------------------
Add function annotations for input type validation / documentation
------------------------------------------------------------------

if type validation and complete swagger documentation is desired,
arguments should be annotated with types.  For Python 3, `function
annotations <https://www.python.org/dev/peps/pep-3107/>`_ are used.

For Python 2, transmute provides an annotate decorator:

.. code-python::

   import transmute_core

   # the python 3 way
   def add(left: int, right: int) -> int:
        return left + right

   # the python 2 way
   @transmute_core.annotate({"left": int, "right": int, "return": int})
   def add(left, right):
       return left + right


----------
Exceptions
----------

.. todo:: ref transmute-core

By default, transmute functions only catch exceptions which extend
transmute_core.APIException, which results in an http response with a
non-200 status code. (typically 400):


.. code-python::

    from transmute_core import APIException

    def my_api() -> int:
        if not retrieve_from_database():
            raise transmute_core

However, many transmute frameworks allow the catching of additional exceptions.
