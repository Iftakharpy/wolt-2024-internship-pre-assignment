from fastapi.testclient import TestClient
from http import HTTPStatus
from ..main import app


client = TestClient(app)


def test_docs_redirect():
    response = client.get("/", follow_redirects=False)
    assert response.status_code == HTTPStatus.PERMANENT_REDIRECT
    assert response.headers["location"] == "/docs"
