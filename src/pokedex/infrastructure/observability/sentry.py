"""Sentry bootstrap."""

import sentry_sdk

from sentry_sdk.integrations.fastapi import FastApiIntegration
from sentry_sdk.integrations.logging import LoggingIntegration


def init_sentry(
    *,
    dsn: str | None,
    enabled: bool,
    environment: str,
    release: str | None,
    service_name: str,
    traces_sample_rate: float = 0.0,
    profiles_sample_rate: float = 0.0,
    send_default_pii: bool = False,
) -> None:
    """Initialize Sentry integration."""
    if not enabled or not dsn:
        return

    # Capture warnings+errors as breadcrumbs; errors go as events
    logging_integration = LoggingIntegration(
        level=None,  # breadcrumbs from std logging; set if you want
        event_level=None,  # let exceptions drive events; or set to logging.ERROR
    )

    sentry_sdk.init(
        dsn=dsn,
        environment=environment,
        release=release,
        integrations=[
            FastApiIntegration(),
            logging_integration,
        ],
        traces_sample_rate=traces_sample_rate,
        profiles_sample_rate=profiles_sample_rate,
        send_default_pii=send_default_pii,
        server_name=service_name,
        # Enable sending logs to Sentry
        enable_logs=True,
        # Set profile_lifecycle to "trace" to automatically
        # run the profiler on when there is an active transaction
        profile_lifecycle="trace",
    )
