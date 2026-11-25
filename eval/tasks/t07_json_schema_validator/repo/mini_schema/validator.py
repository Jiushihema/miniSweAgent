from .types import check_type


def validate(data, schema: dict, path: str = "") -> list[str]:
    errors: list[str] = []
    expected_type = schema.get("type")
    if expected_type and not check_type(data, expected_type):
        errors.append(f"{path or 'root'}: expected {expected_type}")
        return errors

    if expected_type == "object" and isinstance(data, dict):
        for req in schema.get("required", []):
            if req not in data:
                errors.append(f"{req}: missing required field")
        props = schema.get("properties", {})
        for k, subschema in props.items():
            if k in data:
                # BUG: loses parent path prefix
                errors.extend(validate(data[k], subschema, k))
        # BUG: ignores additionalProperties == False

    if expected_type == "array" and isinstance(data, list) and "items" in schema:
        for idx, item in enumerate(data):
            errors.extend(validate(item, schema["items"], f"[{idx}]"))

    return errors
