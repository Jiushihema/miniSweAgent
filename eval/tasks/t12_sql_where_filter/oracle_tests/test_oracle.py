from sql_filter import filter_rows


def test_precedence_in_and_null():
    rows = [
        {"id": 1, "role": "admin", "age": None},
        {"id": 2, "role": "user", "age": 25},
        {"id": 3, "role": "guest", "age": 30},
    ]
    res = filter_rows(rows, "role = 'admin' OR role IN ('user', 'mod') AND age > 20")
    assert [r["id"] for r in res] == [1, 2]
    null_res = filter_rows(rows, "age IS NULL OR (role = 'guest' AND age IS NOT NULL)")
    assert [r["id"] for r in null_res] == [1, 3]
