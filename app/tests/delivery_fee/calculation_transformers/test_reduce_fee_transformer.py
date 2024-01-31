import pytest
from app.delivery_fee.models import DeliveryFee, OrderInfo
from app.delivery_fee.fee_transformers import (
    ReduceFeeTransformer,
)
from app.delivery_fee import settings as settings


@pytest.fixture
def reduce_fee_transformer():
    return ReduceFeeTransformer(settings.EXCLUDE_FEE_CONFIG_OPTIONS)


def test__exclude_fee_transformer_no_exclusion_applied(reduce_fee_transformer: ReduceFeeTransformer):
    current_fee = DeliveryFee(delivery_fee=10e2)
    expected_fee = current_fee + 0

    order_info = OrderInfo(
        cart_value=1,
        delivery_distance=0,
        number_of_items=0,
        time="2024-01-30T13:00:00Z"
    )
    delivery_fee = reduce_fee_transformer.transform(
        order_info,
        current_fee
    )
    # Cart value is 1, so no exclusion should be applied.
    assert delivery_fee == expected_fee


def test__exclude_fee_transformer_exclusion_applied(reduce_fee_transformer: ReduceFeeTransformer):
    current_fee = DeliveryFee(delivery_fee=10e2)
    expected_fee = DeliveryFee(delivery_fee=0)

    order_info = OrderInfo(
        cart_value=settings.EXCLUDE_FEE_CONFIG_OPTIONS.exclusion_cart_value_threshold,
        delivery_distance=0,
        number_of_items=0,
        time="2024-01-30T13:00:00Z"
    )
    delivery_fee = reduce_fee_transformer.transform(
        order_info,
        current_fee
    )
    # Cart value is 200€, so exclusion should be applied.
    assert delivery_fee == expected_fee


def test__exclude_fee_transformer_exclusion_applied_with_over_threshold(reduce_fee_transformer: ReduceFeeTransformer):
    current_fee = DeliveryFee(delivery_fee=10e2)
    expected_fee = DeliveryFee(delivery_fee=0)

    order_info = OrderInfo(
        cart_value=settings.EXCLUDE_FEE_CONFIG_OPTIONS.exclusion_cart_value_threshold + 1,
        delivery_distance=0,
        number_of_items=0,
        time="2024-01-30T13:00:00Z"
    )
    delivery_fee = reduce_fee_transformer.transform(
        order_info,
        current_fee
    )
    # Cart value is 200€, so exclusion should be applied.
    assert delivery_fee == expected_fee
