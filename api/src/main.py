from os import getenv

from fastapi import FastAPI

from .analytics.router import router as analytics_router
from .movies.router import router as movies_router

SENTRY_DSN = getenv('SENTRY_DSN')


if SENTRY_DSN:
    import sentry_sdk
    sentry_sdk.init(
        dsn=SENTRY_DSN,
        send_default_pii=True,
        traces_sample_rate=1.0,
        _experiments={
            "continuous_profiling_auto_start": True,
        },
    )

app = FastAPI(
    debug=getenv('API_DEBUG', False),
)

app.include_router(movies_router)
app.include_router(analytics_router)
