from datetime import datetime


def parse_field(field: str, min_val: int, max_val: int) -> set[int]:
    values: set[int] = set()
    for part in field.split(","):
        if part == "*":
            values.update(range(min_val, max_val + 1))
        elif part.startswith("*/"):
            step = int(part[2:])
            values.update(range(min_val, max_val + 1, step))
        elif "-" in part:
            lo, hi = map(int, part.split("-", 1))
            values.update(range(lo, hi + 1))
        else:
            values.add(int(part))
    return values


def cron_matches(expr: str, dt: datetime) -> bool:
    fields = expr.split()
    if len(fields) != 5:
        raise ValueError("Expected 5 cron fields")
    mins = parse_field(fields[0], 0, 59)
    hours = parse_field(fields[1], 0, 23)
    doms = parse_field(fields[2], 1, 31)
    months = parse_field(fields[3], 1, 12)
    dows = parse_field(fields[4], 0, 6)
    cron_dow = (dt.weekday() + 1) % 7
    return (
        dt.minute in mins
        and dt.hour in hours
        and dt.day in doms
        and dt.month in months
        and cron_dow in dows
    )
