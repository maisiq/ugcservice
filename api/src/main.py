from fastapi import FastAPI

from .movies.router import router as main_router
from .analytics.router import router as analytics_router


app = FastAPI(
    debug=True,
)

app.include_router(main_router)
app.include_router(analytics_router)
