from ratelimit import SlidingWindowLimiter


def test_basic_allow():
    t = [0.0]
    lim = SlidingWindowLimiter(2, 10.0, clock=lambda: t[0])
    assert lim.allow("u1") is True
    assert lim.allow("u1") is True
