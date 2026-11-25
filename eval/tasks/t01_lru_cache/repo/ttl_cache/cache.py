import time
from collections import OrderedDict
from typing import Any, Callable


class TTLCache:
    def __init__(self, capacity: int, ttl_seconds: float, clock: Callable[[], float] = time.monotonic):
        if capacity <= 0:
            raise ValueError("capacity must be positive")
        self.capacity = capacity
        self.ttl_seconds = ttl_seconds
        self._clock = clock
        self._store: OrderedDict[str, tuple[Any, float]] = OrderedDict()

    def get(self, key: str) -> Any:
        if key not in self._store:
            return None
        val, expires_at = self._store[key]
        if self._clock() >= expires_at:
            # BUG: returns None without deleting expired key
            return None
        self._store.move_to_end(key)
        return val

    def set(self, key: str, value: Any) -> None:
        now = self._clock()
        expires_at = now + self.ttl_seconds
        if key in self._store:
            # BUG: keeps old expires_at and doesn't move_to_end
            _, old_exp = self._store[key]
            self._store[key] = (value, old_exp)
            return
        if len(self._store) >= self.capacity:
            # BUG: evicts LRU even when expired entries could be purged first
            self._store.popitem(last=False)
        self._store[key] = (value, expires_at)

    def __len__(self) -> int:
        return len(self._store)
