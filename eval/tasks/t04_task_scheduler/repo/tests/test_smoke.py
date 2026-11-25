from dag_sched import schedule


def test_linear_chain():
    assert schedule({"b": ["a"], "a": []}) == ["a", "b"]
