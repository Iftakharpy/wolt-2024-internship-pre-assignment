import pytest
from fastapi.testclient import TestClient
from http import HTTPStatus
from app.main import app
from app.delivery_fee.models import OrderInfo
import json


@pytest.fixture
def client():
    return TestClient(app)


def test_cart_value_for_lt_10(client: TestClient):
    order_info = OrderInfo(
        cart_value=8.9e2,
        delivery_distance=0,
        number_of_items=0,
        time="2024-01-15T13:00:00Z"
    )
    json_request_data = json.loads(order_info.model_dump_json())
    res = client.post("/api/delivery/calculate_delivery_fee/",
                      json=json_request_data)

    assert res.status_code == HTTPStatus.OK
    assert res.json() == {"delivery_fee": 1.10e2}


def test_cart_value_for_gt_10(client: TestClient):
    order_info = OrderInfo(
        cart_value=10.1e2,
        delivery_distance=0,
        number_of_items=0,
        time="2024-01-15T13:00:00Z"
    )
    json_request_data = json.loads(order_info.model_dump_json())
    res = client.post("/api/delivery/calculate_delivery_fee/",
                      json=json_request_data)

    assert res.status_code == HTTPStatus.OK
    assert res.json() == {"delivery_fee": 0}


def test_delivery_distance_for_lt_1km(client: TestClient):
    order_info = OrderInfo(
        cart_value=0,
        delivery_distance=9.9e2,
        number_of_items=0,
        time="2024-01-15T13:00:00Z"
    )
    json_request_data = json.loads(order_info.model_dump_json())
    res = client.post("/api/delivery/calculate_delivery_fee/",
                      json=json_request_data)

    assert res.status_code == HTTPStatus.OK
    assert res.json() == {"delivery_fee": 2e2 + 10e2}


def test_delivery_distance_for_gt_1km(client: TestClient):
    order_info = OrderInfo(
        cart_value=0,
        delivery_distance=10.1e2,
        number_of_items=0,
        time="2024-01-15T13:00:00Z"
    )
    json_request_data = json.loads(order_info.model_dump_json())
    res = client.post("/api/delivery/calculate_delivery_fee/",
                      json=json_request_data)

    assert res.status_code == HTTPStatus.OK
    assert res.json() == {"delivery_fee": 2e2 + 10e2 + 1e2}


def test_delivery_distance_for_1499m(client: TestClient):
    order_info = OrderInfo(
        cart_value=0,
        delivery_distance=1.499e3,
        number_of_items=0,
        time="2024-01-15T13:00:00Z"
    )
    json_request_data = json.loads(order_info.model_dump_json())
    res = client.post("/api/delivery/calculate_delivery_fee/",
                      json=json_request_data)

    assert res.status_code == HTTPStatus.OK
    assert res.json() == {"delivery_fee": 10e2 + (2e2 + 1e2)}


def test_delivery_distance_for_1500m(client: TestClient):
    order_info = OrderInfo(
        cart_value=0,
        delivery_distance=1.5e3,
        number_of_items=0,
        time="2024-01-15T13:00:00Z"
    )
    json_request_data = json.loads(order_info.model_dump_json())
    res = client.post("/api/delivery/calculate_delivery_fee/",
                      json=json_request_data)

    assert res.status_code == HTTPStatus.OK
    assert res.json() == {"delivery_fee": 10e2 + (2e2 + 1e2)}


def test_delivery_distance_for_1501m(client: TestClient):
    order_info = OrderInfo(
        cart_value=0,
        delivery_distance=1.501e3,
        number_of_items=0,
        time="2024-01-15T13:00:00Z"
    )
    json_request_data = json.loads(order_info.model_dump_json())
    res = client.post("/api/delivery/calculate_delivery_fee/",
                      json=json_request_data)

    assert res.status_code == HTTPStatus.OK
    assert res.json() == {"delivery_fee": 10e2 + (2e2 + 1e2 + 1e2)}


def test_delivery_distance_for_2000m(client: TestClient):
    order_info = OrderInfo(
        cart_value=0,
        delivery_distance=2e3,
        number_of_items=0,
        time="2024-01-15T13:00:00Z"
    )
    json_request_data = json.loads(order_info.model_dump_json())
    res = client.post("/api/delivery/calculate_delivery_fee/",
                      json=json_request_data)

    assert res.status_code == HTTPStatus.OK
    assert res.json() == {"delivery_fee": 10e2 + (2e2 + 1e2 + 1e2)}


def test_delivery_distance_for_2001m(client: TestClient):
    order_info = OrderInfo(
        cart_value=0,
        delivery_distance=2.001e3,
        number_of_items=0,
        time="2024-01-15T13:00:00Z"
    )
    json_request_data = json.loads(order_info.model_dump_json())
    res = client.post("/api/delivery/calculate_delivery_fee/",
                      json=json_request_data)

    assert res.status_code == HTTPStatus.OK
    assert res.json() == {"delivery_fee": 10e2 + (2e2 + 1e2 + 1e2 + 1e2)}


def test_number_of_items_lt_5(client: TestClient):
    order_info = OrderInfo(
        cart_value=0,
        delivery_distance=0,
        number_of_items=4,
        time="2024-01-15T13:00:00Z"
    )
    json_request_data = json.loads(order_info.model_dump_json())

    res = client.post("/api/delivery/calculate_delivery_fee/",
                      json=json_request_data)

    assert res.status_code == HTTPStatus.OK
    assert res.json() == {"delivery_fee": 10e2}


def test_number_of_items_eq_5(client: TestClient):
    order_info = OrderInfo(
        cart_value=0,
        delivery_distance=0,
        number_of_items=5,
        time="2024-01-15T13:00:00Z"
    )
    json_request_data = json.loads(order_info.model_dump_json())

    res = client.post("/api/delivery/calculate_delivery_fee/",
                      json=json_request_data)

    assert res.status_code == HTTPStatus.OK
    assert res.json() == {"delivery_fee": 10e2 + 0.5e2}


def test_number_of_items_for_10(client: TestClient):
    order_info = OrderInfo(
        cart_value=0,
        delivery_distance=0,
        number_of_items=10,
        time="2024-01-15T13:00:00Z"
    )
    json_request_data = json.loads(order_info.model_dump_json())

    res = client.post("/api/delivery/calculate_delivery_fee/",
                      json=json_request_data)

    assert res.status_code == HTTPStatus.OK
    assert res.json() == {"delivery_fee": 10e2 + (0.5e2*(10-4))}


def test_number_of_items_for_13(client: TestClient):
    order_info = OrderInfo(
        cart_value=0,
        delivery_distance=0,
        number_of_items=13,
        time="2024-01-15T13:00:00Z"
    )
    json_request_data = json.loads(order_info.model_dump_json())

    res = client.post("/api/delivery/calculate_delivery_fee/",
                      json=json_request_data)

    assert res.status_code == HTTPStatus.OK
    assert res.json() == {"delivery_fee": min((10e2 + (0.5e2*(13-4)) + 1.2e2), 15e2)}


def test_number_of_items_for_14(client: TestClient):
    order_info = OrderInfo(
        cart_value=0,
        delivery_distance=0,
        number_of_items=14,
        time="2024-01-15T13:00:00Z"
    )
    json_request_data = json.loads(order_info.model_dump_json())

    res = client.post("/api/delivery/calculate_delivery_fee/",
                      json=json_request_data)

    assert res.status_code == HTTPStatus.OK
    assert res.json() == {"delivery_fee": 15e2}


def test_delivery_fee_never_gt_15euro(client: TestClient):
    order_info = OrderInfo(
        cart_value=0,
        delivery_distance=0,
        number_of_items=100,
        time="2024-01-15T13:00:00Z"
    )
    json_request_data = json.loads(order_info.model_dump_json())

    res = client.post("/api/delivery/calculate_delivery_fee/",
                      json=json_request_data)

    assert res.status_code == HTTPStatus.OK
    assert res.json() == {"delivery_fee": 15e2}


def test_delivery_fee_0_when_cart_value_gte_200euro(client: TestClient):
    order_info = OrderInfo(
        cart_value=200e2,
        delivery_distance=15000,
        number_of_items=3000,
        time="2024-01-15T13:00:00Z"
    )
    json_request_data = json.loads(order_info.model_dump_json())

    res = client.post("/api/delivery/calculate_delivery_fee/",
                      json=json_request_data)

    assert res.status_code == HTTPStatus.OK
    assert res.json() == {"delivery_fee": 0}


def test_friday_rush_hour_fee_for_12h(client: TestClient):
    order_info = OrderInfo(
        cart_value=5e2,
        delivery_distance=0,
        number_of_items=0,
        time="2024-02-02T13:00:00Z"
    )
    json_request_data = json.loads(order_info.model_dump_json())

    res = client.post("/api/delivery/calculate_delivery_fee/",
                      json=json_request_data)
    assert res.status_code == HTTPStatus.OK
    assert res.json() == {"delivery_fee": 5e2}


def test_friday_rush_hour_fee_for_15h(client: TestClient):
    order_info = OrderInfo(
        cart_value=5e2,
        delivery_distance=0,
        number_of_items=0,
        time="2024-02-02T15:00:00Z"
    )
    json_request_data = json.loads(order_info.model_dump_json())

    res = client.post("/api/delivery/calculate_delivery_fee/",
                      json=json_request_data)
    assert res.status_code == HTTPStatus.OK
    assert res.json() == {"delivery_fee": 5e2*1.2}


def test_friday_rush_hour_fee_for_end_of_19h(client: TestClient):
    order_info = OrderInfo(
        cart_value=5e2,
        delivery_distance=0,
        number_of_items=0,
        time="2024-02-02T19:59:59Z"
    )
    json_request_data = json.loads(order_info.model_dump_json())

    res = client.post("/api/delivery/calculate_delivery_fee/",
                      json=json_request_data)
    assert res.status_code == HTTPStatus.OK
    assert res.json() == {"delivery_fee": 5e2*1.2}


def test_friday_rush_hour_fee_after_19h(client: TestClient):
    order_info = OrderInfo(
        cart_value=5e2,
        delivery_distance=0,
        number_of_items=0,
        time="2024-02-02T20:00:00Z"
    )
    json_request_data = json.loads(order_info.model_dump_json())

    res = client.post("/api/delivery/calculate_delivery_fee/",
                      json=json_request_data)
    assert res.status_code == HTTPStatus.OK
    assert res.json() == {"delivery_fee": 5e2}


def test_not_friday_rush_hour_fee_for_12h(client: TestClient):
    order_info = OrderInfo(
        cart_value=5e2,
        delivery_distance=0,
        number_of_items=0,
        time="2024-02-02T13:00:00Z"
    )
    json_request_data = json.loads(order_info.model_dump_json())

    res = client.post("/api/delivery/calculate_delivery_fee/",
                      json=json_request_data)
    assert res.status_code == HTTPStatus.OK
    assert res.json() == {"delivery_fee": 5e2}


def test_not_friday_rush_hour_fee_for_15h(client: TestClient):
    order_info = OrderInfo(
        cart_value=5e2,
        delivery_distance=0,
        number_of_items=0,
        time="2024-02-02T15:00:00Z"
    )
    json_request_data = json.loads(order_info.model_dump_json())

    res = client.post("/api/delivery/calculate_delivery_fee/",
                      json=json_request_data)
    assert res.status_code == HTTPStatus.OK
    assert res.json() == {"delivery_fee": 5e2*1.2}


def test_not_friday_rush_hour_fee_for_end_of_19h(client: TestClient):
    order_info = OrderInfo(
        cart_value=5e2,
        delivery_distance=0,
        number_of_items=0,
        time="2024-02-02T19:59:59Z"
    )
    json_request_data = json.loads(order_info.model_dump_json())

    res = client.post("/api/delivery/calculate_delivery_fee/",
                      json=json_request_data)
    assert res.status_code == HTTPStatus.OK
    assert res.json() == {"delivery_fee": 5e2*1.2}


def test_not_friday_rush_hour_fee_after_19h(client: TestClient):
    order_info = OrderInfo(
        cart_value=5e2,
        delivery_distance=0,
        number_of_items=0,
        time="2024-02-02T20:00:00Z"
    )
    json_request_data = json.loads(order_info.model_dump_json())

    res = client.post("/api/delivery/calculate_delivery_fee/",
                      json=json_request_data)
    assert res.status_code == HTTPStatus.OK
    assert res.json() == {"delivery_fee": 5e2}
