from event_bus import EventBus


def test_exact_emit():
    bus = EventBus()
    seen = []
    bus.subscribe("a.b", lambda t, p: seen.append((t, p)))
    bus.emit("a.b", 1)
    assert seen == [("a.b", 1)]
