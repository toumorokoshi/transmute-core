from transmute_core.exceptions import APIException, SerializationException


def test_serialization_error_is_api_exception():
    """
    a serialization exception should
    be considered in the default exceptions
    of the api.
    """
    assert isinstance(SerializationException(""), APIException)
