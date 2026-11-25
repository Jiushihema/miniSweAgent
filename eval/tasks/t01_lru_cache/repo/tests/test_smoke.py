from ttl_cache import TTLCache


def test_basic_set_get():
    t = [0.0]
    c = TTLCache(2, 10.0, clock=lambda: t[0])
    c.set("a", 1)
    assert c.get("a") == 1
