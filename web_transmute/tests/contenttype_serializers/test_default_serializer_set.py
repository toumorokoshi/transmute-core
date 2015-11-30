def test_default_serializer_json(serializer_set):
    frm, expected_to = {"foo": "bar"}, b'{"foo": "bar"}'
    assert serializer_set.to_type("application/json", frm) == expected_to


def test_default_serializer_yaml(serializer_set):
    frm, expected_to = {"foo": "bar"}, b'foo: bar\n'
    assert serializer_set.to_type("application/json", frm) == expected_to
