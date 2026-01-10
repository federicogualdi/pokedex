"""Keyed locks module."""

import asyncio


class KeyedAsyncLocks:
    """Async locks per key to avoid request stampede on cache-miss."""

    def __init__(self) -> None:
        """Initialize locks class."""
        self._locks: dict[str, asyncio.Lock] = {}
        self._guard = asyncio.Lock()

    async def lock_for(self, key: str) -> asyncio.Lock:
        """Lock key to avoid request stampede on cache-miss."""
        async with self._guard:
            lock = self._locks.get(key)
            if lock is None:
                lock = asyncio.Lock()
                self._locks[key] = lock
            return lock
