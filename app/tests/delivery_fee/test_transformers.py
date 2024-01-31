from app.delivery_fee.models import DeliveryFee, OrderInfo
from app.delivery_fee.fee_transformers import (
    RushHourFeeTransformer,
    ReduceFeeTransformer,
    LimitFeeTransformer,
)


def test__friday_rush_hour_fee_transformer():
    friday_rush_hour_fee_transformer = RushHourFeeTransformer()
    order_info = OrderInfo(
        cart_value=0,
        delivery_distance=0,
        number_of_items=0,
        time="2024-01-30T13:00:00Z"  # Not Friday and not rush hour
    )
    delivery_fee = friday_rush_hour_fee_transformer.transform(
        order_info,
        DeliveryFee(delivery_fee=2e2)
    )
    # Delivery time is not Friday and not in rush hour range, so no surcharge is applied.
    assert delivery_fee == DeliveryFee(delivery_fee=2e2)

    order_info = OrderInfo(
        cart_value=0,
        delivery_distance=0,
        number_of_items=0,
        time="2024-01-30T16:00:00Z"  # Not Friday but in rush hour range
    )
    delivery_fee = friday_rush_hour_fee_transformer.transform(
        order_info,
        DeliveryFee(delivery_fee=0)
    )
    # Delivery time is not Friday but in the range of rush hour,
    # so no surcharge should not be applied.
    assert delivery_fee == DeliveryFee(delivery_fee=0)

    order_info = OrderInfo(
        cart_value=0,
        delivery_distance=0,
        number_of_items=0,
        time="2024-01-26T13:00:00Z"
    )
    delivery_fee = friday_rush_hour_fee_transformer.transform(
        order_info,
        DeliveryFee(delivery_fee=0)
    )
    # Delivery time is Friday but not rush hour,
    # so surcharge should not be applied.
    assert delivery_fee == DeliveryFee(delivery_fee=0)

    order_info = OrderInfo(
        cart_value=5e2,
        delivery_distance=0,
        number_of_items=0,
        time="2024-01-26T15:00:00Z"  # Friday and in rush hour range
    )
    delivery_fee = DeliveryFee(delivery_fee=10e2 - 5e2)
    transformed_delivery_fee = friday_rush_hour_fee_transformer.transform(
        order_info,
        delivery_fee
    )
    # Delivery time is Friday but not rush hour,
    # so surcharge should not be applied.
    assert transformed_delivery_fee == (delivery_fee * 1.2)

    order_info = OrderInfo(
        cart_value=5e2,
        delivery_distance=0,
        number_of_items=0,
        time="2024-01-26T19:00:00Z"  # Friday and in rush hour range
    )
    delivery_fee = DeliveryFee(delivery_fee=10e2 - 5e2)
    transformed_delivery_fee = friday_rush_hour_fee_transformer.transform(
        order_info,
        delivery_fee
    )
    # Delivery time is Friday but not rush hour,
    # so surcharge should not be applied.
    assert transformed_delivery_fee == (delivery_fee * 1.2)

    order_info = OrderInfo(
        cart_value=5e2,
        delivery_distance=0,
        number_of_items=0,
        time="2024-01-26T20:00:00Z"  # Friday and in rush hour range
    )
    delivery_fee = DeliveryFee(delivery_fee=10e2 - 5e2)
    transformed_delivery_fee = friday_rush_hour_fee_transformer.transform(
        order_info,
        delivery_fee
    )
    # Delivery time is Friday but not rush hour,
    # so surcharge should not be applied.
    assert transformed_delivery_fee == delivery_fee


def test__exclude_fee_transformer():
    exclude_fee_transformer = ReduceFeeTransformer()
    order_info = OrderInfo(
        cart_value=0,
        delivery_distance=0,
        number_of_items=0,
        time="2024-01-30T13:00:00Z"
    )
    delivery_fee = exclude_fee_transformer.transform(
        order_info,
        DeliveryFee(delivery_fee=0)
    )
    # Cart value is 0, so no exclusion should be applied.
    assert delivery_fee == DeliveryFee(delivery_fee=0)

    order_info = OrderInfo(
        cart_value=200e2,
        delivery_distance=0,
        number_of_items=0,
        time="2024-01-30T13:00:00Z"
    )
    delivery_fee = exclude_fee_transformer.transform(
        order_info,
        DeliveryFee(delivery_fee=0)
    )
    # Cart value is 200€, so exclusion should be applied.
    assert delivery_fee == DeliveryFee(delivery_fee=0)

    order_info = OrderInfo(
        cart_value=200e2 + 1,
        delivery_distance=0,
        number_of_items=0,
        time="2024-01-30T13:00:00Z"
    )
    delivery_fee = exclude_fee_transformer.transform(
        order_info,
        DeliveryFee(delivery_fee=0)
    )
    # Cart value is 200€, so exclusion should be applied.
    assert delivery_fee == DeliveryFee(delivery_fee=0)


def test__limit_fee_transformer():
    limit_fee_transformer = LimitFeeTransformer()
    order_info = OrderInfo(
        cart_value=0,
        delivery_distance=0,
        number_of_items=0,
        time="2024-01-30T13:00:00Z"
    )
    delivery_fee = limit_fee_transformer.transform(
        order_info,
        DeliveryFee(delivery_fee=0)
    )
    # Delivery fee is below limit, so no limit should be applied.
    assert delivery_fee == DeliveryFee(delivery_fee=0)

    order_info = OrderInfo(
        cart_value=0,
        delivery_distance=0,
        number_of_items=0,
        time="2024-01-30T13:00:00Z"
    )
    delivery_fee = limit_fee_transformer.transform(
        order_info,
        DeliveryFee(delivery_fee=15e2)
    )
    # Delivery fee is 15€, so no limit should be applied.
    assert delivery_fee == DeliveryFee(delivery_fee=15e2)

    order_info = OrderInfo(
        cart_value=0,
        delivery_distance=0,
        number_of_items=0,
        time="2024-01-30T13:00:00Z"
    )
    delivery_fee = limit_fee_transformer.transform(
        order_info,
        DeliveryFee(delivery_fee=15e2 + 1)
    )
    # Delivery fee is over 15€, so it should be transformed to 15€.
    assert delivery_fee == DeliveryFee(delivery_fee=15e2)
