import pytest
from dag_sched import schedule


def test_lexicographical_order():
    deps = {"c": ["a"], "b": ["a"], "a": [], "d": ["b", "c"]}
    assert schedule(deps) == ["a", "b", "c", "d"]


def test_cycle_raises():
    with pytest.raises(ValueError):
        schedule({"a": ["b"], "b": ["a"]})


def test_self_cycle_raises():
    with pytest.raises(ValueError):
        schedule({"a": ["a"]})


def test_unknown_dep_raises():
    with pytest.raises(KeyError):
        schedule({"a": ["missing"]})
