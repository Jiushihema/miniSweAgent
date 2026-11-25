import re
from dataclasses import dataclass

LOG_RE = re.compile(r"^(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}) \[([A-Z]+)\] (.*)$")


@dataclass
class LogEntry:
    timestamp: str
    level: str
    message: str


def parse_logs(text: str) -> list[LogEntry]:
    entries: list[LogEntry] = []
    for line in text.splitlines():
        m = LOG_RE.match(line)
        if m:
            entries.append(LogEntry(timestamp=m.group(1), level=m.group(2), message=m.group(3)))
        # BUG: continuation lines (tracebacks) are silently dropped
    return entries
