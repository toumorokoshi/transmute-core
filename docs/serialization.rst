=============
Serialization
=============

transmute-core provides a framework and default implementation to
allow serializing objects to and from common data representation for
an API. This is by chaining two parts:

1. object serialization to / from basic Python data types.
2. data types serialization to / from standard data notations (e.g. json or yaml)

.. todo:: ref TransmuteContext

Both of these components are customizable, either through passing a new
TransmuteContext object, or modifying the default instance.
