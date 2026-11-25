from ttl_cache import TTLCache


def test_purge_expired_before_lru_eviction():
    t = [0.0]
    c = TTLCache(2, 5.0, clock=lambda: t[0])
    c.set("a", 1)
    t[0] = 3.0
    c.set("b", 2)
    t[0] = 7.5  # "a" is expired, "b" is alive
    c.set("c", 3)
    assert c.get("a") is None
    assert c.get("b") == 2
    assert c.get("c") == 3
    assert len(c) == 2


def test_update_refreshes_ttl_and_recency():
    t = [0.0]
    c = TTLCache(2, 5.0, clock=lambda: t[0])
    c.set("a", 1)
    t[0] = 2.0
    c.set("b", 2)
    t[0] = 4.0
    c.set("a", 10)  # refresh "a" -> expires at 9.0, now "b" is LRU
    t[0] = 7.5
    assert c.get("a") == 10
    assert c.get("b") is None  # expired and deleted
    assert len(c) == 1
