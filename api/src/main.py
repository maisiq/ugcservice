from os import getenv

from fastapi import FastAPI
import sentry_sdk

from .movies.router import router as main_router
from .analytics.router import router as analytics_router


SENTRY_DSN = getenv('SENTRY_DSN')


if SENTRY_DSN:
    sentry_sdk.init(
        dsn=SENTRY_DSN,
        send_default_pii=True,
        traces_sample_rate=1.0,
        _experiments={
            "continuous_profiling_auto_start": True,
        },
    )

app = FastAPI(
    debug=True,
)

app.include_router(main_router)
app.include_router(analytics_router)
