from event_bus import EventBus


def test_wildcards_and_once_iteration():
    bus = EventBus()
    log = []
    bus.subscribe("user.*", lambda t, p: log.append(("star", t)), once=True)
    bus.subscribe("user.#", lambda t, p: log.append(("hash", t)))
    bus.emit("user.login", None)
    bus.emit("user.profile.edit", None)
    bus.emit("user", None)
    assert log == [
        ("star", "user.login"),
        ("hash", "user.login"),
        ("hash", "user.profile.edit"),
        ("hash", "user"),
    ]
