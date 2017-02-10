class TransmuteAttributes(object):

    def __init__(self, paths=None, methods=None,
                 query_parameters=None, body_parameters=None,
                 header_parameters=None, path_parameters=None,
                 error_exceptions=None, response_types=None,
                 success_code=200):
        self.paths = set(paths or [])
        self.methods = set(methods or ["GET"])
        self.success_code = success_code
        self.query_parameters = set(query_parameters or [])
        self.body_parameters = set(body_parameters or [])
        self.header_parameters = set(header_parameters or [])
        self.path_parameters = set(path_parameters or [])
        self.error_exceptions = set(error_exceptions or [])
        self.response_types = response_types or {}

    def __or__(self, other):
        """
        merge values from another transmute function, taking the
        union of the two sets.
        """
        paths = self.paths | other.paths
        methods = self.methods | other.methods
        success_code = other.success_code or self.success_code
        query_parameters = self.query_parameters | other.query_parameters
        body_parameters = self.body_parameters | other.body_parameters
        header_parameters = self.header_parameters | other.header_parameters
        path_parameters = self.path_parameters | other.path_parameters
        error_exceptions = self.error_exceptions | other.error_exceptions
        response_types = self.response_types.copy()
        for k, v in other.response_types.items():
            response_types[k] = v
        return TransmuteAttributes(paths, methods,
                                   query_parameters,
                                   body_parameters,
                                   header_parameters,
                                   path_parameters,
                                   error_exceptions,
                                   response_types,
                                   success_code)

    def __str__(self):
        arg_list = []
        for k in ["paths", "methods",
                  "query_parameters", "body_parameters",
                  "header_parameters", "path_parameters",
                  "error_exceptions", "response_types",
                  "success_code"]:
            arg_list.append("{0}={1}".format(
                k, getattr(self, k)
            ))
        return "<TransmuteAttributes {0}>".format(" ".join(arg_list))
