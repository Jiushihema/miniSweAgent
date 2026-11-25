from log_analyzer import parse_logs


def test_parse_single():
    entries = parse_logs("2026-11-01 10:00:00 [INFO] hello\n")
    assert len(entries) == 1
    assert entries[0].level == "INFO"
