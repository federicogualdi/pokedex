"""Test retry."""

import pytest

from _pytest.monkeypatch import MonkeyPatch

from pokedex.infrastructure.resilience.retry import RetryPolicy
from pokedex.infrastructure.resilience.retry import with_retry
from pokedex.shared.exceptions import UpstreamClientError
from pokedex.shared.exceptions import UpstreamServerError


@pytest.mark.asyncio
async def test_with_retry_retries_on_server_error_then_succeeds(monkeypatch: MonkeyPatch):
    """Test retry server error."""
    sleeps: list[float] = []

    async def fake_sleep(s: float) -> None:
        sleeps.append(s)

    monkeypatch.setattr("pokedex.infrastructure.resilience.retry.asyncio.sleep", fake_sleep)

    calls = {"n": 0}

    async def flaky_call() -> str:
        calls["n"] += 1
        if calls["n"] < 3:
            raise UpstreamServerError(service="X", method="GET", path="/p", status_code=500)
        return "OK"

    policy = RetryPolicy(attempts=3, base_delay_s=0.01, max_delay_s=0.02, jitter_s=0.0)
    result = await with_retry(flaky_call, policy)

    assert result == "OK"
    assert calls["n"] == 3
    # due sleep (tra 1->2, 2->3)
    assert len(sleeps) == 2


@pytest.mark.asyncio
async def test_with_retry_does_not_retry_on_client_error(monkeypatch: MonkeyPatch):
    """Test no retry on client error."""

    async def fake_sleep(_: float) -> None:
        raise AssertionError("sleep should not be called for non-retriable errors")

    monkeypatch.setattr("pokedex.infrastructure.resilience.retry.asyncio.sleep", fake_sleep)

    calls = {"n": 0}

    async def bad_call():
        calls["n"] += 1
        raise UpstreamClientError(service="X", method="GET", path="/p", status_code=404)

    policy = RetryPolicy(attempts=5, base_delay_s=0.01, max_delay_s=0.02, jitter_s=0.0)

    with pytest.raises(UpstreamClientError):
        await with_retry(bad_call, policy)

    assert calls["n"] == 1  # nessun retry


@pytest.mark.asyncio
async def test_with_retry_exhausts_attempts_and_raises_last(monkeypatch: MonkeyPatch):
    """Test retry after limit."""

    async def fake_sleep(_: float) -> None:
        return None

    monkeypatch.setattr("pokedex.infrastructure.resilience.retry.asyncio.sleep", fake_sleep)

    calls = {"n": 0}

    async def always_fails():
        calls["n"] += 1
        raise UpstreamServerError(service="X", method="GET", path="/p", status_code=503)

    policy = RetryPolicy(attempts=3, base_delay_s=0.01, max_delay_s=0.02, jitter_s=0.0)

    with pytest.raises(UpstreamServerError):
        await with_retry(always_fails, policy)

    assert calls["n"] == 3
