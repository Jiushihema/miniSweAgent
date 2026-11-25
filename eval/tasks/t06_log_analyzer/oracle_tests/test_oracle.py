from log_analyzer import parse_logs, filter_by_level, top_errors


def test_multiline_and_stats():
    raw = (
        "2026-11-01 10:00:00 [INFO] ok\n"
        "2026-11-01 10:00:01 [ERROR] Boom\n"
        "Traceback:\n"
        "  line 1\n"
        "2026-11-01 10:00:02 [CRITICAL] Alpha\n"
        "2026-11-01 10:00:03 [ERROR] Alpha\n"
    )
    entries = parse_logs(raw)
    assert len(entries) == 4
    assert "Traceback:\n  line 1" in entries[1].message
    errs = filter_by_level(entries, "ERROR")
    assert len(errs) == 3
    assert top_errors(entries, 2) == [("Alpha", 2), ("Boom", 1)]
