from mini_router import Router


def test_static_priority_and_405():
    r = Router()
    r.add("GET", "/users/:id", "by_id")
    r.add("GET", "/users/me", "me")
    assert r.resolve("GET", "/users/me/") == (200, "me", {})
    assert r.resolve("POST", "/users/42") == (405, None, {})
    assert r.resolve("GET", "/unknown") == (404, None, {})
