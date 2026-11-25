def eval_simple(row: dict, clause: str) -> bool:
    for op in ("!=", "=", ">", "<"):
        if op in clause:
            col, raw_val = [x.strip() for x in clause.split(op, 1)]
            val = raw_val.strip("'\"") if raw_val.startswith(("'", '"')) else int(raw_val)
            cell = row.get(col)
            if op == "=":
                return cell == val
            if op == "!=":
                return cell != val
            if op == ">":
                return cell > val
            if op == "<":
                return cell < val
    raise ValueError(f"Unsupported clause: {clause}")


def filter_rows(rows: list[dict], where: str) -> list[dict]:
    out = []
    for row in rows:
        parts = [p.strip() for p in where.split(" AND ")]
        if all(eval_simple(row, p) for p in parts):
            out.append(row)
    return out
