from fastapi.testclient import TestClient
from http import HTTPStatus
from app.main import app


client = TestClient(app)


def test__cart_value__less_than_0():
    response = client.post("/api/delivery/calculate_delivery_fee/",
                           json={
                               "cart_value": -1,
                               "delivery_distance": 0,
                               "number_of_items": 0,
                               "time": "2024-01-15T13:00:00Z"
                           })
    assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY


def test__cart_value__invalid_data_types():
    # Try string
    string_res = client.post("/api/delivery/calculate_delivery_fee/",
                             json={
                                 "cart_value": "invalid",
                                 "delivery_distance": 0,
                                 "number_of_items": 0,
                                 "time": "2024-01-15T13:00:00Z"
                             })
    assert string_res.status_code == HTTPStatus.UNPROCESSABLE_ENTITY

    # Try None/null
    none_res = client.post("/api/delivery/calculate_delivery_fee/",
                           json={
                               "cart_value": None,
                               "delivery_distance": 0,
                               "number_of_items": 0,
                               "time": "2024-01-15T13:00:00Z"
                           })
    assert none_res.status_code == HTTPStatus.UNPROCESSABLE_ENTITY

    # Try boolean
    bool_res = client.post("/api/delivery/calculate_delivery_fee/",
                           json={
                               "cart_value": True,
                               "delivery_distance": 0,
                               "number_of_items": 0,
                               "time": "2024-01-15T13:00:00Z"
                           })
    # Expecting ok since it is quite common to interpret
    # True as 1 and False as 0
    assert bool_res.status_code == HTTPStatus.OK

    # Try list
    list_res = client.post("/api/delivery/calculate_delivery_fee/",
                           json={
                               "cart_value": [1, 2, 3],
                               "delivery_distance": 0,
                               "number_of_items": 0,
                               "time": "2024-01-15T13:00:00Z"
                           })
    assert list_res.status_code == HTTPStatus.UNPROCESSABLE_ENTITY

    # Try dict
    dict_res = client.post("/api/delivery/calculate_delivery_fee/",
                           json={
                               "cart_value": {"a": 1, "b": 2},
                               "delivery_distance": 0,
                               "number_of_items": 0,
                               "time": "2024-01-15T13:00:00Z"
                           })
    assert dict_res.status_code == HTTPStatus.UNPROCESSABLE_ENTITY


def test__delivery_distance__less_than_0():
    response = client.post("/api/delivery/calculate_delivery_fee/",
                           json={
                               "cart_value": 0,
                               "delivery_distance": -10,
                               "number_of_items": 0,
                               "time": "2024-01-15T13:00:00Z"
                           })
    assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY


def test__delivery_distance__invalid_data_types():
    # Try string
    string_res = client.post("/api/delivery/calculate_delivery_fee/",
                             json={
                                 "cart_value": 0,
                                 "delivery_distance": "invalid",
                                 "number_of_items": 0,
                                 "time": "2024-01-15T13:00:00Z"
                             })
    assert string_res.status_code == HTTPStatus.UNPROCESSABLE_ENTITY

    # Try None/null
    none_res = client.post("/api/delivery/calculate_delivery_fee/",
                           json={
                               "cart_value": 0,
                               "delivery_distance": None,
                               "number_of_items": 0,
                               "time": "2024-01-15T13:00:00Z"
                           })
    assert none_res.status_code == HTTPStatus.UNPROCESSABLE_ENTITY

    # Try boolean
    bool_res = client.post("/api/delivery/calculate_delivery_fee/",
                           json={
                               "cart_value": 0,
                               "delivery_distance": False,
                               "number_of_items": 0,
                               "time": "2024-01-15T13:00:00Z"
                           })
    # Expecting ok since it is quite common to interpret
    # True as 1 and False as 0
    assert bool_res.status_code == HTTPStatus.OK

    # Try list
    list_res = client.post("/api/delivery/calculate_delivery_fee/",
                           json={
                               "cart_value": 0,
                               "delivery_distance": [0, 1, 3],
                               "number_of_items": 0,
                               "time": "2024-01-15T13:00:00Z"
                           })
    assert list_res.status_code == HTTPStatus.UNPROCESSABLE_ENTITY

    # Try dict
    dict_res = client.post("/api/delivery/calculate_delivery_fee/",
                           json={
                               "cart_value": 0,
                               "delivery_distance": {"a": 1, "b": 2},
                               "number_of_items": 0,
                               "time": "2024-01-15T13:00:00Z"
                           })
    assert dict_res.status_code == HTTPStatus.UNPROCESSABLE_ENTITY


def test__number_of_items__less_than_0():
    response = client.post("/api/delivery/calculate_delivery_fee/",
                           json={
                               "cart_value": 0,
                               "delivery_distance": 0,
                               "number_of_items": -10,
                               "time": "2024-01-15T13:00:00Z"
                           })
    assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY


def test__number_of_items__invalid_data_types():
    # Try string
    string_res = client.post("/api/delivery/calculate_delivery_fee/",
                             json={
                                 "cart_value": 0,
                                 "delivery_distance": 0,
                                 "number_of_items": "invalid",
                                 "time": "2024-01-15T13:00:00Z"
                             })
    assert string_res.status_code == HTTPStatus.UNPROCESSABLE_ENTITY

    # Try None/null
    none_res = client.post("/api/delivery/calculate_delivery_fee/",
                           json={
                               "cart_value": 0,
                               "delivery_distance": 0,
                               "number_of_items": None,
                               "time": "2024-01-15T13:00:00Z"
                           })
    assert none_res.status_code == HTTPStatus.UNPROCESSABLE_ENTITY

    # Try boolean
    bool_res = client.post("/api/delivery/calculate_delivery_fee/",
                           json={
                               "cart_value": 0,
                               "delivery_distance": 0,
                               "number_of_items": True,
                               "time": "2024-01-15T13:00:00Z"
                           })
    # Expecting ok since it is quite common to interpret
    # True as 1 and False as 0
    assert bool_res.status_code == HTTPStatus.OK

    # Try list
    list_res = client.post("/api/delivery/calculate_delivery_fee/",
                           json={
                               "cart_value": 0,
                               "delivery_distance": 0,
                               "number_of_items": [0, 1, 3],
                               "time": "2024-01-15T13:00:00Z"
                           })
    assert list_res.status_code == HTTPStatus.UNPROCESSABLE_ENTITY

    # Try dict
    dict_res = client.post("/api/delivery/calculate_delivery_fee/",
                           json={
                               "cart_value": 0,
                               "delivery_distance": 0,
                               "number_of_items": {"a": 1, "b": 2},
                               "time": "2024-01-15T13:00:00Z"
                           })
    assert dict_res.status_code == HTTPStatus.UNPROCESSABLE_ENTITY


def test__time__invalid_format():
    response = client.post("/api/delivery/calculate_delivery_fee/",
                           json={
                               "cart_value": 0,
                               "delivery_distance": 0,
                               "number_of_items": 0,
                               "time": "invalid"
                           })
    assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY


def test__time__invalid_data_types():
    # Try string
    string_res = client.post("/api/delivery/calculate_delivery_fee/",
                             json={
                                 "cart_value": 0,
                                 "delivery_distance": 0,
                                 "number_of_items": 0,
                                 "time": "invalid"
                             })
    assert string_res.status_code == HTTPStatus.UNPROCESSABLE_ENTITY

    # Try None/null
    none_res = client.post("/api/delivery/calculate_delivery_fee/",
                           json={
                               "cart_value": 0,
                               "delivery_distance": 0,
                               "number_of_items": 0,
                               "time": None
                           })
    assert none_res.status_code == HTTPStatus.UNPROCESSABLE_ENTITY

    # Try boolean
    bool_res = client.post("/api/delivery/calculate_delivery_fee/",
                           json={
                               "cart_value": 0,
                               "delivery_distance": 0,
                               "number_of_items": 0,
                               "time": True
                           })
    assert bool_res.status_code == HTTPStatus.UNPROCESSABLE_ENTITY

    # Try list
    list_res = client.post("/api/delivery/calculate_delivery_fee/",
                           json={
                               "cart_value": 0,
                               "delivery_distance": 0,
                               "number_of_items": 0,
                               "time": [0, 1, 3]
                           })
    assert list_res.status_code == HTTPStatus.UNPROCESSABLE_ENTITY

    # Try dict
    dict_res = client.post("/api/delivery/calculate_delivery_fee/",
                           json={
                               "cart_value": 0,
                               "delivery_distance": 0,
                               "number_of_items": 0,
                               "time": {"a": 1, "b": 2}
                           })
    assert dict_res.status_code == HTTPStatus.UNPROCESSABLE_ENTITY
