from datetime import datetime
from cron_match import cron_matches


def test_step_range_sunday7_and_or_semantics():
    # 2026-11-22 is Sunday, day 22
    sun = datetime(2026, 11, 22, 10, 3)
    assert cron_matches("1-10/2 10 * * 7", sun) is True
    # Restricted DOM (1) OR restricted DOW (0=Sunday) -> matches Sunday Nov 22
    assert cron_matches("3 10 1 * 0", sun) is True
    # Neither DOM=1 nor DOW=1 (Mon) matches Sunday Nov 22
    assert cron_matches("3 10 1 * 1", sun) is False
