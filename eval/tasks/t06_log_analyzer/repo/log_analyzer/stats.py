from collections import Counter
from .parser import LogEntry

LEVEL_ORDER = {"DEBUG": 10, "INFO": 20, "WARNING": 30, "ERROR": 40, "CRITICAL": 50}


def filter_by_level(entries: list[LogEntry], min_level: str) -> list[LogEntry]:
    threshold = LEVEL_ORDER[min_level]
    # BUG: uses > instead of >=
    return [e for e in entries if LEVEL_ORDER.get(e.level, 0) > threshold]


def top_errors(entries: list[LogEntry], n: int = 5) -> list[tuple[str, int]]:
    # BUG: only counts ERROR (misses CRITICAL), uses full multiline message, no tie-break
    counts = Counter(e.message for e in entries if e.level == "ERROR")
    return counts.most_common(n)
