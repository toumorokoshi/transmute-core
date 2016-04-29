.. transmute-core documentation master file, created by
   sphinx-quickstart on Fri Apr 15 00:25:27 2016.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

transmute-core
=============

transmute-core is a library designed to help create "transmute" toolboxes for
web frameworks. A transmute toolbox provides the following:

* declarative generation of http handler interfaces by parsing :doc:`function <function signatures>`.
* validation and serialization to and from a variety of content types (e.g. json or yaml).
* validation and serialization to and from native python objects, using `schematics <http://schematics.readthedocs.org/en/latest/>`_.
* documentation of all handlers generated this way, via `swagger <http://swagger.io/>`_.

Contents:

If you are interested in adding a transmute toolbox for your preferred
web framework, please read :ref:`authoring_a_toolbox`

.. toctree::
   :maxdepth: 2
   authoring_a_toolbox



Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
