from fastapi import FastAPI

from src.routes.routes import router as main_router


app = FastAPI(
    debug=True,
)

app.include_router(main_router)
