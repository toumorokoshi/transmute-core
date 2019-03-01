=====
Serialization and Validation
=====

As part of the API construction, tranmsute-core handles validating the incoming payload to match a schema, and serialization of the json or yaml payloads into native Python types.

transmute does not provide it's own schema definition or validation system. Instead, it hooks into several existing options, extracting json schemas and relying on their validation mechanism.

These types are matches to arguments using python type annotations, or the @transmure_core.annotate decorator.

At a high level, the following are supported:

* python primitive types
* `attrs <http://www.attrs.org/en/stable/>`_ objects that use type annotations or have a type argument to attr.ib.
* types denoted using the `typing <https://docs.python.org/3/library/typing.html>`_ module (installed as a separate package for python versions older than 3.5)
* `schematics <http://schematics.readthedocs.org/en/latest/>`_ models and types.

The following discusses the types in detail.

Python Primitives
=================

The following primitives can be used directly:

* bool
* float
* int
* str
* decimal
* datetime

Typing Module
=============

Anything from the typing module is supported.

Attrs
=====

Attrs provides a way to define types per attr.ib, which can be parsed
by transmute. subtypes can be a combination of attrs objects, or the typing module. E.g. to define a list of attrs objects, you can use typing.List[MyAttrsClass].

Schematics
==========

Both schematics models, and schematics types are supported. 

(note: benchmarking has shows schematics to be very imperformant. See performance).

Details
=======

Query Parameter Array Arguments as Comma-separated List
--------------------------------------------------------------------

The intention is to ensure that serialization and deserialization of types matches
that of `openapi <https://www.openapis.org/>`_, to ensure that the UI provided is usable.

This forces behaviors such as multiple arguments being consumed as a comma-separated argument
per query parameter, rather than just as multiple query parameter with the same name.

Performance
===========

Among all of the components within transmute-core, the serialization and validation component has the most overhead (the rest are negligible relative to most application's business logic). As a result, the choice of object to use will have a huge impact on performance.

attrs is the most performant, with a huge con around error messages (a missing argument return back a wrong number of arguments passed into __init__).

schematics has great error messages, but is roughly 30x slower than attrs.

Customization
=============

transmute-core can support additional object types, by modifying the global TransmuteContext object.

Both of these components are customizable, either through passing a new
TransmuteContext object, or modifying the default instance.

To learn more about customizing these serializers, please see the API reference
for TransmuteContext, ObjectSerializer, and ContentTypeSerializer.