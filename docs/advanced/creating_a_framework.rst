=====================================
Creating a framework-specific library
=====================================

----------------------------------------
Full framework in 100 statements or less
----------------------------------------

The reuse achieved in transmute-core has allowed the
framework-specific libraries to be extremely thin: Initial
integrations of Flask and aiohttp were achieved in less than 100
statements of python code.

If you find yourself writing a lot of code to integrate with
transmute-core, consider sending an issue: there may be more
functionality that can be contributed to the core to enable a thinner
layer.

--------
Overview
--------

A transmute library should provide at a minimum the following functionality:

1. a way to convert a transmute_function to a handler for your framework of choice.
2. a way to register a transmute function to the application object
3. a way to generate a swagger.json from an application object

See transmute_core.frameworks for examples

.. important:

   transmute-core is deliberately minimal on integration with a framework (such as using
   route decorators a la Flask, or creating handler classes like Tornado). It's recommended
   to implement apis that work well when used with however routes are declared and
   generated in the target framework.

--------------
Simple Example
--------------


Here is a minimal implementation for `Flask <http://flask.pocoo.org/>`_, clocking in at
just under 200 lines including comments and formatting. (just under 100 without)

.. include:: ../../example.py
    :literal:
