from mini_schema import validate


def test_bool_not_int_and_nested_paths_and_additional():
    schema = {
        "type": "object",
        "additionalProperties": False,
        "required": ["user", "items"],
        "properties": {
            "user": {
                "type": "object",
                "properties": {"age": {"type": "integer"}},
                "required": ["age"],
            },
            "items": {
                "type": "array",
                "items": {"type": "object", "properties": {"id": {"type": "integer"}}},
            },
        },
    }
    errs = validate({"user": {"age": True}, "items": [{"id": 1}, {"id": "bad"}], "extra": 1}, schema)
    joined = "\n".join(errs)
    assert "user.age" in joined
    assert "items[1].id" in joined
    assert "extra" in joined
