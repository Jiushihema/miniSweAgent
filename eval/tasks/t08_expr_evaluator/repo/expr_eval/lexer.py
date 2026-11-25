import re

TOKEN_RE = re.compile(r"\s*(?:(\d+(?:\.\d+)?)|(\*\*|//|[+\-*/%()])|(\S))")


def tokenize(text: str) -> list[tuple[str, str]]:
    tokens: list[tuple[str, str]] = []
    for num, op, bad in TOKEN_RE.findall(text):
        if bad:
            raise ValueError(f"Unexpected char: {bad}")
        if num:
            tokens.append(("NUM", num))
        elif op:
            tokens.append((op, op))
    return tokens
