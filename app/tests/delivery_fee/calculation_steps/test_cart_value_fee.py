import pytest
from app.delivery_fee.models import DeliveryFee, OrderInfo
from app.delivery_fee.fee_calculation_steps import (
    CartValueFee
)
import app.delivery_fee.settings as settings


@pytest.fixture
def cart_value_fee():
    return CartValueFee(settings.CART_VALUE_CONFIG_OPTIONS)


def test__cart_value_fee_applies_surcharge(cart_value_fee: CartValueFee):
    expected_fee = 300

    order_info = OrderInfo(
        cart_value=settings.CART_VALUE_CONFIG_OPTIONS.cart_value_surcharge_threshold - expected_fee,
        delivery_distance=0,
        number_of_items=0,
        time="2024-01-15T13:00:00Z"
    )
    delivery_fee = cart_value_fee.calculate(order_info)
    # Cart value is less than 10€, so surcharge is applied.
    assert delivery_fee == DeliveryFee(delivery_fee=expected_fee)


def test__cart_value_fee_no_surcharge(cart_value_fee: CartValueFee):
    order_info = OrderInfo(
        cart_value=settings.CART_VALUE_CONFIG_OPTIONS.cart_value_surcharge_threshold,
        delivery_distance=0,
        number_of_items=0,
        time="2024-01-15T13:00:00Z"
    )
    delivery_fee = cart_value_fee.calculate(order_info)
    # Cart value is equal to 10€, so no surcharge is applied.
    assert delivery_fee == DeliveryFee(delivery_fee=0)


def test__cart_value_fee_test_case_from_example(cart_value_fee: CartValueFee):
    order_info = OrderInfo(
        cart_value=8.9e2,
        delivery_distance=0,
        number_of_items=0,
        time="2024-01-15T13:00:00Z"
    )
    delivery_fee = cart_value_fee.calculate(order_info)
    # Test case from example
    assert delivery_fee == DeliveryFee(delivery_fee=1.1e2)


def test__cart_value_fee_over_threshold(cart_value_fee: CartValueFee):
    expected_fee = 0

    order_info = OrderInfo(
        cart_value=settings.CART_VALUE_CONFIG_OPTIONS.cart_value_surcharge_threshold + 1,
        delivery_distance=0,
        number_of_items=0,
        time="2024-01-15T13:00:00Z"
    )
    delivery_fee = cart_value_fee.calculate(order_info)

    # Cart value is more than 10€, so no surcharge is applied.
    assert delivery_fee == DeliveryFee(delivery_fee=expected_fee)
