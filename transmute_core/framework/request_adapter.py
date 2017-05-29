class RequestAdapter(object):
    """
    RequestAdapters bridge transmute's
    representation of a request, with the framework's
    implementation.

    implement the unimplemented methods.
    """

    @property
    def body(self):
        """ return the request body. """
        raise NotImplementedError()

    def _get_framework_args(self):
        """
        often, a framework provides specific variables that are passed
        into the handler function (e.g. the request object in
        aiohttp). return a dictionary of these arguments, which will be
        added to the function arguments if they appear.
        """
        raise NotImplementedError()

    def _query_argument(self, key, is_list):
        raise NotImplementedError()

    def _header_argument(self, key):
        raise NotImplementedError()

    def _path_argument(self, key):
        raise NotImplementedError()
