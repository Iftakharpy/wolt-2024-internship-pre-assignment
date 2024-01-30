from fastapi.testclient import TestClient
from http import HTTPStatus
from ..main import app


client = TestClient(app)


def test__cart_value_invalid_data_type():
    response = client.post("/api/delivery/calculate_delivery_fee/",
                           json={
                               "cart_value": "-1",
                               "delivery_distance": 2235,
                               "number_of_items": 4,
                               "delivery_time": "2024-01-15T13:00:00Z"
                           })
    assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY
