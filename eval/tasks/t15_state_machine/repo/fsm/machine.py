from typing import Callable


class StateMachine:
    def __init__(self, initial: str):
        self.state = initial
        self._transitions: dict[tuple[str, str], tuple[str, Callable | None]] = {}
        self._on_enter: dict[str, list[Callable]] = {}
        self._on_exit: dict[str, list[Callable]] = {}

    def add_transition(self, src: str, event: str, dst: str, guard: Callable | None = None) -> None:
        self._transitions[(src, event)] = (dst, guard)

    def on_enter(self, state: str, fn: Callable) -> None:
        self._on_enter.setdefault(state, []).append(fn)

    def on_exit(self, state: str, fn: Callable) -> None:
        self._on_exit.setdefault(state, []).append(fn)

    def trigger(self, event: str, ctx: dict | None = None) -> str:
        key = (self.state, event)
        if key not in self._transitions:
            raise ValueError(f"Invalid transition: {key}")
        dst, guard = self._transitions[key]
        for fn in self._on_exit.get(self.state, []):
            fn(ctx)
        if guard and not guard(ctx):
            raise PermissionError("Guard rejected")
        self.state = dst
        for fn in self._on_enter.get(dst, []):
            fn(ctx)
        return self.state
