from ratelimit import SlidingWindowLimiter


def test_per_key_and_rejected_not_recorded():
    t = [0.0]
    lim = SlidingWindowLimiter(2, 10.0, clock=lambda: t[0])
    assert lim.allow("u1") is True
    assert lim.allow("u1") is True
    assert lim.allow("u1") is False  # must not record
    assert lim.allow("u2") is True   # independent key
    t[0] = 10.0  # boundary: ts=0.0 is now expired (0.0 <= 10.0 - 10.0)
    assert lim.allow("u1") is True
    assert lim.allow("u1") is True
    assert lim.allow("u1") is False
