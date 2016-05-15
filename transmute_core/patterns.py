"""
Very often, implementing a new transmute framework is a
fill-in-the-blanks project, hooking in the right functions to apply
transmute's functionality.

These module provides some templatized code to assist with that.
"""
from abc import ABCMeta
from .compat import with_metaclass


class RouteGenerator(with_metaclass(ABCMeta, object)):
    """
    To create a compatible route generator, extend this functionality
    and override the methods.
    """
