import pytest
from fastapi.testclient import TestClient
from http import HTTPStatus
from app.main import app


client = TestClient(app)


edge_cases_for_numeric_fields = [-1, -10, 100.5, None,
                                 [1, 2, 3], [], {}, {"a": 1, "b": 2}, "invalid"]


#########################################################################################
# Test cart_value field
#########################################################################################

def test__cart_value_with_valid_data():
    # Try with valid data
    string_res = client.post("/api/delivery/calculate_delivery_fee/",
                             json={
                                 "cart_value": 0,
                                 "delivery_distance": 0,
                                 "number_of_items": 0,
                                 "time": "2024-01-15T13:00:00Z"
                             })
    assert string_res.status_code == HTTPStatus.OK


@pytest.mark.parametrize("cart_value", edge_cases_for_numeric_fields)
def test__cart_value__with_invalid_data_types(cart_value):
    # Try with each of the cart_value values in the list above
    string_res = client.post("/api/delivery/calculate_delivery_fee/",
                             json={
                                 "cart_value": cart_value,
                                 "delivery_distance": 0,
                                 "number_of_items": 0,
                                 "time": "2024-01-15T13:00:00Z"
                             })
    assert string_res.status_code == HTTPStatus.UNPROCESSABLE_ENTITY


def test__cart_value__edge_case_boolean():
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


#########################################################################################
# Test delivery_distance field
#########################################################################################

def test__delivery_distance_with_valid_data():
    # Try with valid data
    string_res = client.post("/api/delivery/calculate_delivery_fee/",
                             json={
                                 "cart_value": 0,
                                 "delivery_distance": 0,
                                 "number_of_items": 0,
                                 "time": "2024-01-15T13:00:00Z"
                             })
    assert string_res.status_code == HTTPStatus.OK


@pytest.mark.parametrize("delivery_distance", edge_cases_for_numeric_fields)
def test__delivery_distance__with_invalid_data_types(delivery_distance):
    # Try with each of the delivery_distance values in the list above
    string_res = client.post("/api/delivery/calculate_delivery_fee/",
                             json={
                                 "cart_value": 0,
                                 "delivery_distance": delivery_distance,
                                 "number_of_items": 0,
                                 "time": "2024-01-15T13:00:00Z"
                             })
    assert string_res.status_code == HTTPStatus.UNPROCESSABLE_ENTITY


def test__delivery_distance__edge_case_boolean():
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


#########################################################################################
# Test number_of_items field
#########################################################################################

def test__number_of_items_with_valid_data():
    # Try with valid data
    string_res = client.post("/api/delivery/calculate_delivery_fee/",
                             json={
                                 "cart_value": 0,
                                 "delivery_distance": 0,
                                 "number_of_items": 0,
                                 "time": "2024-01-15T13:00:00Z"
                             })
    assert string_res.status_code == HTTPStatus.OK


@pytest.mark.parametrize("number_of_items", edge_cases_for_numeric_fields)
def test__number_of_items__with_invalid_data_types(number_of_items):
    # Try with each of the number_of_items values in the list above
    response = client.post("/api/delivery/calculate_delivery_fee/",
                           json={
                               "cart_value": 0,
                               "delivery_distance": 0,
                               "number_of_items": number_of_items,
                               "time": "2024-01-15T13:00:00Z"
                           })
    assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY


def test__number_of_items__edge_case_boolean():
    # Try boolean
    bool_res = client.post("/api/delivery/calculate_delivery_fee/",
                           json={
                               "cart_value": 0,
                               "delivery_distance": 0,
                               "number_of_items": False,
                               "time": "2024-01-15T13:00:00Z"
                           })
    # Expecting ok since it is quite common to interpret
    # True as 1 and False as 0
    assert bool_res.status_code == HTTPStatus.OK


#########################################################################################
# Test time field
#########################################################################################

def test__time_with_valid_data():
    # Try with valid data
    string_res = client.post("/api/delivery/calculate_delivery_fee/",
                             json={
                                 "cart_value": 0,
                                 "delivery_distance": 0,
                                 "number_of_items": 0,
                                 "time": "2024-01-15T13:00:00Z"
                             })
    assert string_res.status_code == HTTPStatus.OK


@pytest.mark.parametrize("time", [edge_cases_for_numeric_fields]+[True])
def test__time__invalid_data_types(time):
    # Try with each of the time values in the list above
    string_res = client.post("/api/delivery/calculate_delivery_fee/",
                             json={
                                 "cart_value": 0,
                                 "delivery_distance": 0,
                                 "number_of_items": 0,
                                 "time": time
                             })
    assert string_res.status_code == HTTPStatus.UNPROCESSABLE_ENTITY
