import time
from typing import Callable


class SlidingWindowLimiter:
    def __init__(self, max_requests: int, window_seconds: float, clock: Callable[[], float] = time.monotonic):
        if max_requests <= 0 or window_seconds <= 0:
            raise ValueError("max_requests and window_seconds must be positive")
        self.max_requests = max_requests
        self.window_seconds = window_seconds
        self._clock = clock
        self._hits: list[float] = []

    def allow(self, key: str) -> bool:
        now = self._clock()
        self._hits = [ts for ts in self._hits if now - ts <= self.window_seconds]
        self._hits.append(now)
        return len(self._hits) <= self.max_requests
