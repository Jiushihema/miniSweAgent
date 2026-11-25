from mini_schema import validate


def test_valid_simple():
    schema = {"type": "object", "properties": {"name": {"type": "string"}}, "required": ["name"]}
    assert validate({"name": "alice"}, schema) == []
