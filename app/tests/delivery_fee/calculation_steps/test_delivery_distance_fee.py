import pytest
from app.delivery_fee.models import DeliveryFee, OrderInfo
from app.delivery_fee.fee_calculation_steps import (
    DeliveryDistanceFee,
)
import app.delivery_fee.settings as settings


@pytest.fixture
def delivery_distance_fee():
    return DeliveryDistanceFee(settings.DELIVERY_DISTANCE_CONFIG_OPTIONS)


def test__delivery_distance_fee_not_applied(delivery_distance_fee: DeliveryDistanceFee):
    expected_fee = 0

    order_info = OrderInfo(
        cart_value=0,
        delivery_distance=0,
        number_of_items=0,
        time="2024-01-15T13:00:00Z"
    )
    delivery_fee = delivery_distance_fee.calculate(order_info)

    # Delivery distance is 0, so no surcharge is applied.
    assert delivery_fee == DeliveryFee(delivery_fee=expected_fee)


def test__delivery_distance_fee_applied_for_first_1km_for_low_value(delivery_distance_fee: DeliveryDistanceFee):
    expected_fee = settings.DELIVERY_DISTANCE_CONFIG_OPTIONS.delivery_distance_surcharge_for_low_threshold

    order_info = OrderInfo(
        cart_value=0,
        delivery_distance=1,
        number_of_items=0,
        time="2024-01-15T13:00:00Z"
    )
    delivery_fee = delivery_distance_fee.calculate(order_info)

    # Delivery distance is 0, so no surcharge is applied.
    assert delivery_fee == DeliveryFee(
        delivery_fee=expected_fee)


def test__delivery_distance_fee_applied_for_first_1km_for_edge_value(delivery_distance_fee: DeliveryDistanceFee):
    expected_fee = settings.DELIVERY_DISTANCE_CONFIG_OPTIONS.delivery_distance_surcharge_for_low_threshold

    order_info = OrderInfo(
        cart_value=0,
        delivery_distance=settings.DELIVERY_DISTANCE_CONFIG_OPTIONS.delivery_distance_low_threshold,
        number_of_items=0,
        time="2024-01-15T13:00:00Z"
    )
    delivery_fee = delivery_distance_fee.calculate(order_info)

    # Delivery distance is 1km, so surcharge is applied.
    assert delivery_fee == DeliveryFee(
        delivery_fee=expected_fee)


def test__delivery_distance_fee_applied_for_first_1km_with_additional_fee(delivery_distance_fee: DeliveryDistanceFee):
    expected_fee = settings.DELIVERY_DISTANCE_CONFIG_OPTIONS.delivery_distance_surcharge_for_low_threshold + \
        settings.DELIVERY_DISTANCE_CONFIG_OPTIONS.additional_fee

    order_info = OrderInfo(
        cart_value=0,
        delivery_distance=settings.DELIVERY_DISTANCE_CONFIG_OPTIONS.delivery_distance_low_threshold + 1,
        number_of_items=0,
        time="2024-01-15T13:00:00Z"
    )
    delivery_fee = delivery_distance_fee.calculate(order_info)

    # Delivery distance is 1.5km, so surcharge is applied.
    assert delivery_fee == DeliveryFee(delivery_fee=expected_fee)


def test__delivery_distance_fee_applied_for_first_1km_with_additional_fee_for_edge_value(delivery_distance_fee: DeliveryDistanceFee):
    expected_fee = settings.DELIVERY_DISTANCE_CONFIG_OPTIONS.delivery_distance_surcharge_for_low_threshold + \
        settings.DELIVERY_DISTANCE_CONFIG_OPTIONS.additional_fee

    order_info = OrderInfo(
        cart_value=0,
        delivery_distance=delivery_distance_fee.config_options.delivery_distance_low_threshold +
        settings.DELIVERY_DISTANCE_CONFIG_OPTIONS.additional_fee_applied_per_meters_traveled,
        number_of_items=0,
        time="2024-01-15T13:00:00Z"
    )
    delivery_fee = delivery_distance_fee.calculate(order_info)

    # Delivery distance is 1.5km, surcharge should be 3 euros.
    assert delivery_fee == DeliveryFee(delivery_fee=expected_fee)


def test__delivery_distance_fee_applied_for_first_1km_with_additional_fee_for_higher_value(delivery_distance_fee: DeliveryDistanceFee):
    additional_fee_multiplier = 5
    expected_fee = (settings.DELIVERY_DISTANCE_CONFIG_OPTIONS.delivery_distance_surcharge_for_low_threshold +
                    (settings.DELIVERY_DISTANCE_CONFIG_OPTIONS.additional_fee*additional_fee_multiplier))

    order_info = OrderInfo(
        cart_value=0,
        delivery_distance=(settings.DELIVERY_DISTANCE_CONFIG_OPTIONS.delivery_distance_low_threshold +
                           (settings.DELIVERY_DISTANCE_CONFIG_OPTIONS.additional_fee_applied_per_meters_traveled*additional_fee_multiplier)),
        number_of_items=0,
        time="2024-01-15T13:00:00Z"
    )

    delivery_distance_fee = DeliveryDistanceFee()
    delivery_fee = delivery_distance_fee.calculate(order_info)
    # delivery fee should be 5*1€ + 2€ = 7€
    assert delivery_fee == DeliveryFee(delivery_fee=expected_fee)
