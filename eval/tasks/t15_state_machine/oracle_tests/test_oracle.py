import pytest
from fsm import StateMachine


def test_guard_order_and_rollback():
    log = []
    m = StateMachine("draft")
    m.add_transition("draft", "publish", "live", guard=lambda ctx: ctx.get("ok", False))
    m.on_exit("draft", lambda ctx: log.append("exit_draft"))

    def bad_enter(ctx):
        log.append("enter_live")
        if ctx.get("boom"):
            raise RuntimeError("fail")

    m.on_enter("live", bad_enter)

    with pytest.raises(PermissionError):
        m.trigger("publish", {"ok": False})
    assert m.state == "draft"
    assert log == []

    with pytest.raises(RuntimeError):
        m.trigger("publish", {"ok": True, "boom": True})
    assert m.state == "draft"
    assert log == ["exit_draft", "enter_live"]
