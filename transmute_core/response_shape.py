from swagger_schema import Schema


class ResponseShape(object):
    """
    result shapes define the return format of the
    response.
    """

    @staticmethod
    def create_body(result_dict):
        """
        given the result dict from
        transmute_func, return back the
        response object.
        """
        raise NotImplementedError()

    @staticmethod
    def swagger(result_schema):
        """
        given the schema of the inner
        result object, return back the
        swagger schema representation.
        """
        raise NotImplementedError()


class ResponseShapeSimple(ResponseShape):
    """ return back just the result object. """

    @staticmethod
    def create_body(result_dict):
        return result_dict["result"]

    @staticmethod
    def swagger(result_schema):
        return result_schema


class ResponseShapeComplex(ResponseShape):
    """
    return back an object with the result nested,
    providing a little more context on the result:

    * status code
    * success
    * result
    """

    @staticmethod
    def create_body(result_dict):
        return result_dict

    @staticmethod
    def swagger(result_schema):
        return Schema({
            "title": "SuccessObject",
            "type": "object",
            "properties": {
                "result": result_schema,
                "success": {"type": "boolean"},
                "code": {"type": "number"}
            },
            "required": ["success", "result", "code"]
        })
