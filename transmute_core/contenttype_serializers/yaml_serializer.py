import yaml
from .interface import ContentTypeSerializer


class YamlSerializer(ContentTypeSerializer):

    @staticmethod
    def to_type(data):
        """
        should return back a bytes (or string in python 2),
        representation of your object, to be used in e.g. response
        bodies.
        """
        return yaml.dump(data, default_flow_style=False).encode("UTF-8")

    @staticmethod
    def from_type(raw_bytes):
        """
        given a bytes object, should return a base python data
        structure that represents the object.
        """
        return yaml.load(raw_bytes)

    @staticmethod
    def can_handle(content_type_name):
        """
        given a content type, returns true if this serializer
        can convert bodies of the given type.
        """
        return "yaml" in content_type_name
