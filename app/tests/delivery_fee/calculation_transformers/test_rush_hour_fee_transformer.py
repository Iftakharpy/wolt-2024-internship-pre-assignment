import pytest
from app.delivery_fee.models import DeliveryFee, OrderInfo
from app.delivery_fee.fee_transformers import (
    RushHourFeeTransformer,
)
from app.delivery_fee import settings as settings


@pytest.fixture
def rush_hour_fee_transformer():
    return RushHourFeeTransformer(settings.FRIDAY_RUSH_HOUR_CONFIG_OPTIONS)


def test__friday_rush_hour_fee_transformer__no_surcharge_applied(rush_hour_fee_transformer: RushHourFeeTransformer):
    current_fee = DeliveryFee(delivery_fee=3e2)
    expected_fee = current_fee + 0

    order_info = OrderInfo(
        cart_value=0,
        delivery_distance=0,
        number_of_items=0,
        time="2024-01-30T13:00:00Z"  # Not Friday and not rush hour
    )
    delivery_fee = rush_hour_fee_transformer.transform(
        order_info,
        current_fee
    )

    # Delivery time is not Friday and not in rush hour range, so no surcharge is applied.
    assert delivery_fee == expected_fee


def test__friday_rush_hour_fee_transformer__no_surcharge_applied_for_different_day(rush_hour_fee_transformer: RushHourFeeTransformer):
    current_fee = DeliveryFee(delivery_fee=3e2)
    expected_fee = current_fee

    order_info = OrderInfo(
        cart_value=0,
        delivery_distance=0,
        number_of_items=0,
        time="2024-01-30T16:00:00Z"  # Not Friday but in rush hour range
    )
    delivery_fee = rush_hour_fee_transformer.transform(
        order_info,
        current_fee
    )

    # Delivery time is not Friday but in the range of rush hour,
    # so no surcharge should not be applied.
    assert delivery_fee == expected_fee


def test__friday_rush_hour_fee_transformer__no_surcharge_applied_for_not_rush(rush_hour_fee_transformer: RushHourFeeTransformer):
    current_fee = DeliveryFee(delivery_fee=3e2)
    expected_fee = current_fee + 0

    order_info = OrderInfo(
        cart_value=0,
        delivery_distance=0,
        number_of_items=0,
        time="2024-01-26T13:00:00Z"
    )
    delivery_fee = rush_hour_fee_transformer.transform(
        order_info,
        current_fee
    )

    # Delivery time is Friday but not rush hour,
    # so surcharge should not be applied.
    assert delivery_fee == expected_fee


def test__friday_rush_hour_fee_transformer__surcharge_applied_in_range(rush_hour_fee_transformer: RushHourFeeTransformer):
    current_fee = DeliveryFee(delivery_fee=3e2)
    expected_fee = current_fee * settings.FRIDAY_RUSH_HOUR_CONFIG_OPTIONS.rush_hour_fee_factor

    order_info = OrderInfo(
        cart_value=5e2,
        delivery_distance=0,
        number_of_items=0,
        time="2024-01-26T15:00:00Z"  # Friday and in rush hour range
    )
    delivery_fee = rush_hour_fee_transformer.transform(
        order_info,
        current_fee
    )
    # Delivery time is Friday but not rush hour,
    # so surcharge should not be applied.
    assert delivery_fee == expected_fee


def test__friday_rush_hour_fee_transformer__surcharge_applied_for_rush_hour_end(rush_hour_fee_transformer: RushHourFeeTransformer):
    current_fee = DeliveryFee(delivery_fee=3e2)
    expected_fee = current_fee * settings.FRIDAY_RUSH_HOUR_CONFIG_OPTIONS.rush_hour_fee_factor

    order_info = OrderInfo(
        cart_value=5e2,
        delivery_distance=0,
        number_of_items=0,
        time="2024-01-26T19:59:59Z"  # Friday and in rush hour range
    )
    delivery_fee = rush_hour_fee_transformer.transform(
        order_info,
        current_fee
    )

    # Delivery time is Friday and rush hour ends at 7:59:59 PM,
    # so surcharge should be applied.
    assert delivery_fee == expected_fee


def test__friday_rush_hour_fee_transformer__surcharge_applied_for_rush_hour_start(rush_hour_fee_transformer: RushHourFeeTransformer):
    current_fee = DeliveryFee(delivery_fee=3e2)
    expected_fee = current_fee * settings.FRIDAY_RUSH_HOUR_CONFIG_OPTIONS.rush_hour_fee_factor

    order_info = OrderInfo(
        cart_value=0,
        delivery_distance=0,
        number_of_items=0,
        time="2024-01-26T15:00:00Z"  # Friday and in rush hour range
    )

    delivery_fee = rush_hour_fee_transformer.transform(
        order_info,
        current_fee
    )
    # Delivery time is Friday and start of rush hour is at 3:00:00 PM,
    # so surcharge should be applied.
    assert delivery_fee == expected_fee


def test__friday_rush_hour_fee_transformer__no_surcharge_applied_for_rush_hour_after_rush_hour_end(rush_hour_fee_transformer: RushHourFeeTransformer):
    current_fee = DeliveryFee(delivery_fee=3e2)
    expected_fee = current_fee + 0

    order_info = OrderInfo(
        cart_value=0,
        delivery_distance=0,
        number_of_items=0,
        time="2024-01-26T20:00:00Z"  # Friday and in rush hour range
    )

    delivery_fee = rush_hour_fee_transformer.transform(
        order_info,
        current_fee
    )
    # Delivery time is Friday and start of rush hour is at 3:00:00 PM,
    # so surcharge should be applied.
    assert delivery_fee == expected_fee
