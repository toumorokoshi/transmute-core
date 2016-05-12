import json
from .interface import ContentTypeSerializer


class JsonSerializer(ContentTypeSerializer):

    content_type = ["application/json"]

    @staticmethod
    def dump(data):
        """
        should return back a bytes (or string in python 2),
        representation of your object, to be used in e.g. response
        bodies.
        """
        return json.dumps(data).encode("UTF-8")

    @staticmethod
    def load(raw_bytes):
        """
        given a bytes object, should return a base python data
        structure that represents the object.
        """
        return json.loads(raw_bytes.decode("UTF-8"))

    @staticmethod
    def can_handle(content_type_name):
        """
        given a content type, returns true if this serializer
        can convert bodies of the given type.
        """
        return "json" in content_type_name
