from transmute_core.function.attributes import TransmuteAttributes


def test_merge():
    left = TransmuteAttributes(
        methods=["POST"], query_parameters=["a"]
    )
    right = TransmuteAttributes(
        methods=["PUT"], query_parameters=["b"],
        body_parameters=["c"]
    )
    joined = left | right
    assert joined.methods == set(["POST", "PUT"])
    assert joined.query_parameters == set(["a", "b"])
    assert joined.body_parameters == set(["c"])
