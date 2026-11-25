from mini_router import Router


def test_basic_route():
    r = Router()
    r.add("GET", "/users/:id", "get_user")
    assert r.resolve("GET", "/users/42") == (200, "get_user", {"id": "42"})
