class TransmuteAttributes(object):

    def __init__(self, paths=None, methods=None,
                 query_parameters=None, body_parameters=None,
                 header_parameters=None, path_parameters=None,
                 error_exceptions=None):
        self.paths = set(paths or [])
        self.methods = set(methods or ["GET"])
        self.query_parameters = set(query_parameters or [])
        self.body_parameters = set(body_parameters or [])
        self.header_parameters = set(header_parameters or [])
        self.path_parameters = set(path_parameters or [])
        self.error_exceptions = set(error_exceptions or [])

    def __or__(self, other):
        """
        merge values from another transmute function, taking the
        union of the two sets.
        """
        paths = self.paths | other.paths
        methods = self.methods | other.methods
        query_parameters = self.query_parameters | other.query_parameters
        body_parameters = self.body_parameters | other.body_parameters
        header_parameters = self.header_parameters | other.header_parameters
        path_parameters = self.path_parameters | other.path_parameters
        error_exceptions = self.error_exceptions | other.error_exceptions
        return TransmuteAttributes(paths, methods,
                                   query_parameters,
                                   body_parameters,
                                   header_parameters,
                                   path_parameters,
                                   error_exceptions)

    def __str__(self):
        arg_list = []
        for k in ["paths", "methods",
                  "query_parameters", "body_parameters",
                  "header_parameters", "path_parameters",
                  "error_exceptions"]:
            arg_list.append("{0}={1}".format(
                k, getattr(self, k)
            ))
        return "<TransmuteAttributes {0}>".format(" ".join(arg_list))
