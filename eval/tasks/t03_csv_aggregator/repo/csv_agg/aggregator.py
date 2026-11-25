import csv
import io


def aggregate_sum(csv_text: str, group_col: str, value_col: str) -> list[tuple[str, float]]:
    reader = csv.DictReader(io.StringIO(csv_text.strip()))
    totals: dict[str, float] = {}
    for row in reader:
        g = row[group_col]
        v = float(row[value_col])
        totals[g] = totals.get(g, 0.0) + v
    return sorted(totals.items(), key=lambda item: item[1], reverse=True)
