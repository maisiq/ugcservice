from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.responses import JSONResponse

from .analytics.router import router as analytics_router
from .config.config import API_DEBUG, SENTRY_DSN
from .logger.logger import get_logger, init_logger
from .movies.router import router as movies_router
from .producer.producer import init_kafka_producer


def init_sentry():
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


@asynccontextmanager
async def lifespan(app: FastAPI):
    init_logger()
    init_sentry()
    logger = get_logger()
    kafka_producer = await init_kafka_producer()
    yield
    logger.info('Lifespan: Close all connections to Kafka cluster')
    await kafka_producer.stop()


def init() -> FastAPI:
    app = FastAPI(
        debug=API_DEBUG,
        lifespan=lifespan,
    )
    app.include_router(movies_router)
    app.include_router(analytics_router)
    app.add_route('/_ping', healthcheck, methods=['GET'])
    return app


async def healthcheck(r):
    return JSONResponse({'status': 'ok'})
