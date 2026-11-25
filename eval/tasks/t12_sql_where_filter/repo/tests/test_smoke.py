from sql_filter import filter_rows


def test_simple_and():
    rows = [{"a": 1, "b": "x"}, {"a": 2, "b": "y"}]
    assert filter_rows(rows, "a = 1 AND b = 'x'") == [{"a": 1, "b": "x"}]
