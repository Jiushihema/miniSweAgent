from typing import Callable


class EventBus:
    def __init__(self):
        self._subs: list[tuple[str, Callable, bool]] = []

    def subscribe(self, pattern: str, fn: Callable, once: bool = False) -> None:
        self._subs.append((pattern, fn, once))

    def unsubscribe(self, pattern: str, fn: Callable) -> None:
        self._subs = [(p, f, o) for p, f, o in self._subs if not (p == pattern and f == fn)]

    def emit(self, topic: str, payload=None) -> None:
        for idx, (pat, fn, once) in enumerate(self._subs):
            if pat == topic:
                fn(topic, payload)
                if once:
                    self._subs.pop(idx)
