from contextlib import asynccontextmanager

from fastapi.testclient import TestClient
from src.db.mongo_client import get_db_client
from src.logger.logger import init_logger
from src.main import init
from tests.conftest import get_mongodb_client


@asynccontextmanager
async def mock_lifespan(app):
    init_logger()
    yield


app = init()
app.dependency_overrides[get_db_client] = get_mongodb_client
app.router.lifespan_context = mock_lifespan


def test_userdata_endpoint_returns_404(db_client):
    with TestClient(app) as client:
        resp = client.get('/userdata/1')
        assert resp.status_code == 404
