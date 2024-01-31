import pytest
from app.delivery_fee.models import DeliveryFee, OrderInfo
from app.delivery_fee.fee_transformers import (
    LimitFeeTransformer,
)
from app.delivery_fee import settings as settings


@pytest.fixture
def limit_fee_transformer():
    return LimitFeeTransformer(settings.LIMIT_FEE_CONFIG_OPTIONS)


def test__limit_fee_transformer(limit_fee_transformer: LimitFeeTransformer):
    current_fee = DeliveryFee(
        delivery_fee=settings.LIMIT_FEE_CONFIG_OPTIONS.highest_limit_of_delivery_fee-1)
    expected_fee = current_fee + 0

    order_info = OrderInfo(
        cart_value=0,
        delivery_distance=0,
        number_of_items=0,
        time="2024-01-30T13:00:00Z"
    )
    delivery_fee = limit_fee_transformer.transform(
        order_info,
        current_fee
    )
    # Delivery fee is below limit, so no limit should not be applied.
    assert delivery_fee == expected_fee


def test__limit_fee_transformer__edge_value(limit_fee_transformer: LimitFeeTransformer):
    current_fee = DeliveryFee(
        delivery_fee=settings.LIMIT_FEE_CONFIG_OPTIONS.highest_limit_of_delivery_fee)
    expected_fee = current_fee + 0

    order_info = OrderInfo(
        cart_value=0,
        delivery_distance=0,
        number_of_items=0,
        time="2024-01-30T13:00:00Z"
    )
    delivery_fee = limit_fee_transformer.transform(
        order_info,
        current_fee
    )

    # Delivery fee is 15€, so no limit should be applied.
    assert delivery_fee == expected_fee


def test__limit_fee_transformer__limit_applied(limit_fee_transformer: LimitFeeTransformer):
    current_fee = DeliveryFee(delivery_fee=16e2)
    expected_fee = DeliveryFee(
        delivery_fee=settings.LIMIT_FEE_CONFIG_OPTIONS.highest_limit_of_delivery_fee)

    order_info = OrderInfo(
        cart_value=0,
        delivery_distance=0,
        number_of_items=0,
        time="2024-01-30T13:00:00Z"
    )
    delivery_fee = limit_fee_transformer.transform(
        order_info,
        current_fee
    )
    # Delivery fee is over 15€, so it should be transformed to 15€.
    assert delivery_fee == expected_fee
