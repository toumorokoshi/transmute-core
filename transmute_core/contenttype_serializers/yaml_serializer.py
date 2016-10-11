import yaml
from .interface import ContentTypeSerializer
from ..exceptions import SerializationException


class YamlSerializer(ContentTypeSerializer):

    content_type = ["application/x-yaml"]

    @staticmethod
    def dump(data):
        """
        should return back a bytes (or string in python 2),
        representation of your object, to be used in e.g. response
        bodies.
        """
        return yaml.dump(data, default_flow_style=False).encode("UTF-8")

    @classmethod
    def main_type(cls):
        return cls.content_type[0]

    @staticmethod
    def load(raw_bytes):
        """
        given a bytes object, should return a base python data
        structure that represents the object.
        """
        try:
            return yaml.load(raw_bytes)
        except yaml.scanner.ScannerError as e:
            raise SerializationException(str(e))

    @staticmethod
    def can_handle(content_type_name):
        """
        given a content type, returns true if this serializer
        can convert bodies of the given type.
        """
        return "yaml" in content_type_name
