def parse_ini(text: str) -> dict[str, dict[str, str]]:
    result: dict[str, dict[str, str]] = {}
    current_section = None

    for raw_line in text.splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#") or line.startswith(";"):
            continue
        if line.startswith("[") and line.endswith("]"):
            current_section = line[1:-1].strip()
            result.setdefault(current_section, {})
            continue
        if "=" not in line:
            raise ValueError(f"Invalid line: {raw_line!r}")
        key, val = line.split("=", 1)
        key = key.strip()
        # BUG: naively splits on # even inside quotes, doesn't strip quotes or handle None section
        val = val.split("#", 1)[0].strip()
        result.setdefault(current_section, {})[key] = val

    return result
