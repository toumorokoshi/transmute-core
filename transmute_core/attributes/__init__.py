from ..compat import string_type
from ..exceptions import InvalidTransmuteDefinition
from .response_type import ResponseType


class TransmuteAttributes(object):
    def __init__(
        self,
        paths=None,
        methods=None,
        tags=None,
        query_parameters=None,
        body_parameters=None,
        header_parameters=None,
        path_parameters=None,
        error_exceptions=None,
        response_types=None,
        success_code=200,
        parameter_descriptions=None,
    ):
        self.paths = set(paths or [])
        self.methods = set(methods or ["GET"])
        self.tags = set(tags or [])
        self.success_code = success_code
        self.query_parameters = set(query_parameters or [])
        self.body_parameters = self._coerce_parameters(body_parameters)
        self.header_parameters = set(header_parameters or [])
        self.path_parameters = set(path_parameters or [])
        self.error_exceptions = set(error_exceptions or [])
        self.parameter_descriptions = parameter_descriptions or {}
        self.response_types = {}
        for code, response in (response_types or {}).items():
            if not isinstance(response, ResponseType):
                response = ResponseType(**response)
            self.response_types[code] = response

    @staticmethod
    def _coerce_parameters(param):
        if isinstance(param, string_type):
            return param
        elif isinstance(param, set):
            return param
        elif isinstance(param, list):
            return set(param)
        elif isinstance(param, type(None)):
            return set()
        else:
            raise InvalidTransmuteDefinition(
                "parameter must be a string, list or set. found: {0}".format(param)
            )

    def __or__(self, other):
        """
        merge values from another transmute function, taking the
        union of the two sets.
        """
        response_types = self.response_types.copy()
        for k, v in other.response_types.items():
            response_types[k] = v

        parameter_descriptions = self.parameter_descriptions.copy()
        parameter_descriptions.update(other.parameter_descriptions)

        return TransmuteAttributes(
            paths=(self.paths | other.paths),
            methods=(self.methods | other.methods),
            tags=(self.tags | other.tags),
            success_code=(other.success_code or self.success_code),
            query_parameters=(self.query_parameters | other.query_parameters),
            body_parameters=self._join_parameters(
                other.body_parameters, self.body_parameters
            ),
            header_parameters=(self.header_parameters | other.header_parameters),
            path_parameters=(self.path_parameters | other.path_parameters),
            error_exceptions=(self.error_exceptions | other.error_exceptions),
            parameter_descriptions=parameter_descriptions,
            response_types=response_types,
        )

    def __str__(self):
        arg_list = []
        for k in [
            "paths",
            "methods",
            "tags",
            "query_parameters",
            "body_parameters",
            "header_parameters",
            "path_parameters",
            "error_exceptions",
            "response_types",
            "success_code",
            "parameter_descriptions",
        ]:
            arg_list.append("{0}={1}".format(k, getattr(self, k)))
        return "<TransmuteAttributes {0}>".format(" ".join(arg_list))

    @staticmethod
    def _join_parameters(base, nxt):
        """join parameters from the lhs to the rhs, if compatible."""
        if nxt is None:
            return base
        if isinstance(base, set) and isinstance(nxt, set):
            return base | nxt
        else:
            return nxt
