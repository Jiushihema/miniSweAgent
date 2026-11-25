from fsm import StateMachine


def test_basic_transition():
    m = StateMachine("idle")
    m.add_transition("idle", "start", "running")
    assert m.trigger("start") == "running"
