import re


def slugify(title: str) -> str:
    s = title.strip().lower()
    s = re.sub(r"[^a-z0-9\s-]", "", s)
    s = re.sub(r"\s+", "-", s)
    return s


def extract_toc(markdown_text: str) -> list[tuple[int, str, str]]:
    toc: list[tuple[int, str, str]] = []
    for line in markdown_text.splitlines():
        m = re.match(r"^(#{1,6})\s+(.*)$", line)
        if m:
            level = len(m.group(1))
            title = m.group(2).strip()
            toc.append((level, title, slugify(title)))
    return toc
