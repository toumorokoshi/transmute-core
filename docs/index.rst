.. transmute-core documentation master file, created by
   sphinx-quickstart on Fri Apr 15 00:25:27 2016.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

transmute-core
==============

transmute-core is a library designed to help create "transmute"
library for web frameworks. A transmute library provides the
following:

* declarative generation of http handler interfaces by parsing :doc:`route functions <routes>`.
* validation and serialization to and from a variety of content types (e.g. json or yaml).
* validation and serialization to and from native python objects, using `schematics <http://schematics.readthedocs.org/en/latest/>`_.
* :doc:`autodocumentation <autodocumentation>` of all handlers generated this way, via `swagger <http://swagger.io/>`_.

transmute-core is released under the `MIT license <https://github.com/toumorokoshi/transmute-core/blob/master/LICENSE>`_.

If you are interested in adding a transmute toolbox for your preferred
web framework, please read :doc:`authoring_a_toolbox`

User's Guide:

.. toctree::
   :maxdepth: 2

   autodocumentation
   routes
   serialization
   authoring_a_toolbox

API Reference:


.. toctree::
   :maxdepth: 2

   api
