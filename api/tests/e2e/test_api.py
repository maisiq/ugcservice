from fastapi.testclient import TestClient
from src.db.config import get_db_client
from src.main import app
from tests.conftest import get_mongodb_client


app.dependency_overrides[get_db_client] = get_mongodb_client


def test_userdata_endpoint_returns_404(db_client):
    with TestClient(app) as client:
        resp = client.get('/userdata/1')
        assert resp.status_code == 404
