"""Retry method code."""

import asyncio
import random

from collections.abc import Awaitable
from collections.abc import Callable
from dataclasses import dataclass

from pokedex.shared.exceptions import UpstreamRequestError
from pokedex.shared.exceptions import UpstreamServerError
from pokedex.shared.exceptions import UpstreamTimeoutError

_rng = random.SystemRandom()


@dataclass(frozen=True)
class RetryPolicy:
    """Retry policy."""

    attempts: int = 3
    base_delay_s: float = 0.2
    max_delay_s: float = 2.0
    jitter_s: float = 0.2


def is_retriable(exc: Exception) -> bool:
    """Return True if the exception should trigger a retry."""
    return isinstance(
        exc,
        (
            UpstreamServerError,  # 5xx
            UpstreamTimeoutError,  # timeouts
            UpstreamRequestError,  # network/DNS/connection errors
        ),
    )


def _compute_sleep_s(attempt: int, policy: RetryPolicy) -> float:
    """Exponential backoff with jitter.

    attempt is 1-based (1..attempts-1 for sleep computations).
    """
    attempt = max(attempt, 1)

    # exponential backoff: base * 2^(attempt-1), capped
    backoff = policy.base_delay_s * (2 ** (attempt - 1))
    backoff = min(backoff, policy.max_delay_s)

    # jitter in [0, jitter_s)
    jitter = _rng.random() * policy.jitter_s
    return backoff + jitter


async def with_retry[T](
    fn: Callable[[], Awaitable[T]],
    policy: RetryPolicy = RetryPolicy(),
    *,
    should_retry: Callable[[Exception], bool] = is_retriable,
) -> T:
    """Execute `fn` with retries according to policy.

    - Retries only if `should_retry(exc)` is True.
    - Uses exponential backoff + jitter between attempts.
    - Re-raises the last exception when retries are exhausted.
    """
    if policy.attempts < 1:
        # "No attempts" doesn't make sense; treat as 1 attempt.
        policy = RetryPolicy(
            attempts=1,
            base_delay_s=policy.base_delay_s,
            max_delay_s=policy.max_delay_s,
            jitter_s=policy.jitter_s,
        )

    last_exc: Exception | None = None

    for attempt in range(1, policy.attempts + 1):
        try:
            return await fn()
        except Exception as exc:
            last_exc = exc

            # Do not retry if:
            # - retries exhausted, OR
            # - exception is not retriable
            if attempt >= policy.attempts or not should_retry(exc):
                raise

            sleep_s = _compute_sleep_s(attempt, policy)
            await asyncio.sleep(sleep_s)

    raise last_exc  # type: ignore[misc]
