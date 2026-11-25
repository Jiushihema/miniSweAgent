import re

HUNK_RE = re.compile(r"^@@ -(\d+)(?:,(\d+))? \+(\d+)(?:,(\d+))? @@")


def apply_unified_diff(original: str, diff_text: str) -> str:
    lines = original.splitlines()
    offset = 0
    diff_lines = diff_text.splitlines()
    i = 0
    while i < len(diff_lines):
        m = HUNK_RE.match(diff_lines[i])
        if not m:
            i += 1
            continue
        old_start = int(m.group(1)) - 1 + offset
        i += 1
        pos = old_start
        while i < len(diff_lines) and not diff_lines[i].startswith("@@"):
            dl = diff_lines[i]
            if dl.startswith(" "):
                pos += 1
            elif dl.startswith("-"):
                lines.pop(pos)
                offset -= 1
            elif dl.startswith("+"):
                lines.insert(pos, dl[1:])
                pos += 1
                offset += 1
            i += 1
    return "\n".join(lines) + ("\n" if original.endswith("\n") else "")
