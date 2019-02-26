# What is transmute-core?

transmute-core removes the boilerplate of writing well-documented, easy to use APIs for Python web services, and easily integrates with any web framework. It takes a function
that looks like this:

    from transmute_core import annotate
    from transmute_core.frameworks.flask import route

    @route(app, paths='/multiply', tags=['math'])
    def multiply(left: int, right: int) -> int:
        return left * right


Into an API /multiply that:

* validates and serializes objects into the proper object
* has an documentation page for all APIs generated this way, via [swagger](http://swagger.io/).

The example above is for flask, but transmute-core has integrations for:

* [aiohttp](https://github.com/toumorokoshi/aiohttp-transmute/)
* [flask](https://github.com/toumorokoshi/flask-transmute/)
* [tornado](http://www.tornadoweb.org/en/stable/)

To learn more, see the [tutorial](01_tutorial.md).

## License

transmute-core is released under the [MIT license](https://github.com/toumorokoshi/transmute-core/blob/master/LICENSE).

However, transmute-core bundles [swagger-ui](https://github.com/swagger-api/swagger-ui) with it, which is released under
the Apache2 license.