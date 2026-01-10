"""Cache implementation."""

import time

from collections import OrderedDict
from dataclasses import dataclass
from typing import TypeVar

T = TypeVar("T")


@dataclass
class _Entry[T]:
    """Entry for cache."""

    value: T
    expires_at: float


class InMemoryTTLCache[T]:
    """Simple TTL cache with maxsize and LRU-like eviction (process-local)."""

    def __init__(self, *, ttl_seconds: int, maxsize: int):
        """In-Memory cache Init."""
        self._ttl = ttl_seconds
        self._maxsize = maxsize
        self._data: OrderedDict[str, _Entry[T]] = OrderedDict()

    def get(self, key: str) -> T | None:
        """Get entry by key."""
        now = time.time()
        entry = self._data.get(key)
        if entry is None:
            return None

        if entry.expires_at <= now:
            self._data.pop(key, None)
            return None

        # LRU: mark as recently used
        self._data.move_to_end(key, last=True)
        return entry.value

    def set(self, key: str, value: T) -> None:
        """Set entry by key and value."""
        expires_at = time.time() + self._ttl
        self._data[key] = _Entry(value=value, expires_at=expires_at)
        self._data.move_to_end(key, last=True)
        self._evict_if_needed()

    def _evict_if_needed(self) -> None:
        while len(self._data) > self._maxsize:
            self._data.popitem(last=False)
