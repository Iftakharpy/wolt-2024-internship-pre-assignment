import pytest
from app.delivery_fee.models import DeliveryFee, OrderInfo
from app.delivery_fee.fee_calculation_steps import (
    NumberOfItemsFee,
)
from app.delivery_fee import settings as settings


@pytest.fixture
def number_of_items_fee():
    return NumberOfItemsFee(settings.NUMBER_OF_ITEMS_CONFIG_OPTIONS)


def test__number_of_items_fee_for_no_surcharge(number_of_items_fee: NumberOfItemsFee):
    expected_fee = 0

    order_info = OrderInfo(
        cart_value=0,
        delivery_distance=0,
        number_of_items=0,
        time="2024-01-15T13:00:00Z"
    )
    delivery_fee = number_of_items_fee.calculate(order_info)

    # Number of items is 0, so no surcharge is applied.
    assert delivery_fee == DeliveryFee(delivery_fee=expected_fee)


def test__number_of_items_fee_for_no_surcharge_with_edge_value(number_of_items_fee: NumberOfItemsFee):
    expected_fee = 0

    order_info = OrderInfo(
        cart_value=0,
        delivery_distance=0,
        number_of_items=settings.NUMBER_OF_ITEMS_CONFIG_OPTIONS.number_of_items_surcharge_threshold,
        time="2024-01-15T13:00:00Z"
    )
    delivery_fee = number_of_items_fee.calculate(order_info)

    # Number of items is 4, so no surcharge is applied.
    assert delivery_fee == DeliveryFee(delivery_fee=expected_fee)


def test__number_of_items_fee_no_surcharge_lower_than_threshold(number_of_items_fee: NumberOfItemsFee):
    expected_fee = 0
    order_info = OrderInfo(
        cart_value=0,
        delivery_distance=0,
        number_of_items=1,
        time="2024-01-15T13:00:00Z"
    )
    delivery_fee = number_of_items_fee.calculate(order_info)

    # Number of items is 1, so surcharge is applied.
    assert delivery_fee == DeliveryFee(delivery_fee=expected_fee)


def test__number_of_items_fee_no_surcharge_applied(number_of_items_fee: NumberOfItemsFee):
    expected_fee = settings.NUMBER_OF_ITEMS_CONFIG_OPTIONS.surcharge_per_item_over_threshold

    order_info = OrderInfo(
        cart_value=0,
        delivery_distance=0,
        number_of_items=settings.NUMBER_OF_ITEMS_CONFIG_OPTIONS.number_of_items_surcharge_threshold + 1,
        time="2024-01-15T13:00:00Z"
    )
    delivery_fee = number_of_items_fee.calculate(order_info)

    # Number of items is 5, so surcharge is applied.
    assert delivery_fee == DeliveryFee(delivery_fee=expected_fee)


def test__number_of_items_fee_bulk_charge_not_applied_for_edge_before_bulk(number_of_items_fee: NumberOfItemsFee):
    expected_fee = (settings.NUMBER_OF_ITEMS_CONFIG_OPTIONS.surcharge_per_item_over_threshold *
                    (settings.NUMBER_OF_ITEMS_CONFIG_OPTIONS.bulk_charge_threshold -
                     settings.NUMBER_OF_ITEMS_CONFIG_OPTIONS.number_of_items_surcharge_threshold))

    order_info = OrderInfo(
        cart_value=0,
        delivery_distance=0,
        number_of_items=settings.NUMBER_OF_ITEMS_CONFIG_OPTIONS.bulk_charge_threshold,
        time="2024-01-15T13:00:00Z"
    )
    delivery_fee = number_of_items_fee.calculate(order_info)

    # Number of items is 12, so surcharge is applied. Bulk charge
    # is not applied since number of items is not greater than 12.
    assert delivery_fee == DeliveryFee(delivery_fee=expected_fee)


def test__number_of_items_fee_bulk_charge_not_applied_for_items_below_threshold(number_of_items_fee: NumberOfItemsFee):
    number_of_items = 11
    items_over_surcharge_threshold = (number_of_items -
                                      settings.NUMBER_OF_ITEMS_CONFIG_OPTIONS.number_of_items_surcharge_threshold)
    expected_fee = (items_over_surcharge_threshold *
                    settings.NUMBER_OF_ITEMS_CONFIG_OPTIONS.surcharge_per_item_over_threshold)

    order_info = OrderInfo(
        cart_value=0,
        delivery_distance=0,
        number_of_items=number_of_items,
        time="2024-01-15T13:00:00Z"
    )
    delivery_fee = number_of_items_fee.calculate(order_info)

    # Number of items is 11, so surcharge is applied.
    assert delivery_fee == DeliveryFee(delivery_fee=expected_fee)


def test__number_of_items_fee_bulk_charge_applied_for_just_over_threshold(number_of_items_fee: NumberOfItemsFee):
    number_of_items = 13
    items_over_surcharge_threshold = (number_of_items -
                                      settings.NUMBER_OF_ITEMS_CONFIG_OPTIONS.number_of_items_surcharge_threshold)
    expected_fee = ((items_over_surcharge_threshold *
                    settings.NUMBER_OF_ITEMS_CONFIG_OPTIONS.surcharge_per_item_over_threshold) +
                    settings.NUMBER_OF_ITEMS_CONFIG_OPTIONS.bulk_charge)
    order_info = OrderInfo(
        cart_value=0,
        delivery_distance=0,
        number_of_items=13,
        time="2024-01-15T13:00:00Z"
    )
    delivery_fee = number_of_items_fee.calculate(order_info)
    # Number of items is 13, so surcharge is applied. Bulk charge
    # is applied since number of items is greater than 12.
    assert delivery_fee == DeliveryFee(delivery_fee=expected_fee)


def test__number_of_items_fee_bulk_charge_applied_for_bigger_number_of_items(number_of_items_fee: NumberOfItemsFee):
    number_of_items = 100
    items_over_surcharge_threshold = (number_of_items -
                                      settings.NUMBER_OF_ITEMS_CONFIG_OPTIONS.number_of_items_surcharge_threshold)
    expected_fee = ((items_over_surcharge_threshold *
                    settings.NUMBER_OF_ITEMS_CONFIG_OPTIONS.surcharge_per_item_over_threshold) +
                    settings.NUMBER_OF_ITEMS_CONFIG_OPTIONS.bulk_charge)
    order_info = OrderInfo(
        cart_value=0,
        delivery_distance=0,
        number_of_items=number_of_items,
        time="2024-01-15T13:00:00Z"
    )
    delivery_fee = number_of_items_fee.calculate(order_info)

    # Bulk charge and surcharge is applied.
    assert delivery_fee == DeliveryFee(delivery_fee=expected_fee)
