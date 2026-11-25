from datetime import datetime
from cron_match import cron_matches


def test_every_five_min():
    assert cron_matches("*/5 * * * *", datetime(2026, 1, 1, 12, 15)) is True
