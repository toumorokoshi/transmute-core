=======
aiohttp
=======

Concise Example
===============

.. code-block:: python

    from aiohttp import web
    from transmute_core.frameworks.aiohttp import (
        describe, add_swagger, route
    )

    @describe(paths="/multiply")
    async def multiply(request, left: int, right: int) -> int:
        return left * right

    app = web.Application()
    route(app, multiply)
    # this should be at the end, to ensure all routes are considered when
    # constructing the handler.
    add_swagger(app, "/swagger.json", "/swagger")