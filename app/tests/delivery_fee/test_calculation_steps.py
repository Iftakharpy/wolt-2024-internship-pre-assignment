from app.delivery_fee.models import DeliveryFee, OrderInfo
from app.delivery_fee.fee_calculation_steps import (
    CartValueFee,
    DeliveryDistanceFee,
    NumberOfItemsFee,
)


def test__cart_value_fee():
    cart_value_fee = CartValueFee()
    order_info = OrderInfo(
        cart_value=5e2,
        delivery_distance=0,
        number_of_items=0,
        time="2024-01-15T13:00:00Z"
    )
    delivery_fee = cart_value_fee.calculate(order_info)
    # Cart value is less than 10€, so surcharge is applied.
    assert delivery_fee == DeliveryFee(delivery_fee=5e2)

    order_info = OrderInfo(
        cart_value=10e2,
        delivery_distance=0,
        number_of_items=0,
        time="2024-01-15T13:00:00Z"
    )
    delivery_fee = cart_value_fee.calculate(order_info)
    # Cart value is equal to 10€, so no surcharge is applied.
    assert delivery_fee == DeliveryFee(delivery_fee=0)

    order_info = OrderInfo(
        cart_value=8.9e2,
        delivery_distance=0,
        number_of_items=0,
        time="2024-01-15T13:00:00Z"
    )
    delivery_fee = cart_value_fee.calculate(order_info)
    # Test case from example
    assert delivery_fee == DeliveryFee(delivery_fee=1.1e2)


def test__delivery_distance_fee():
    delivery_distance_fee = DeliveryDistanceFee()
    order_info = OrderInfo(
        cart_value=0,
        delivery_distance=0,
        number_of_items=0,
        time="2024-01-15T13:00:00Z"
    )
    delivery_fee = delivery_distance_fee.calculate(order_info)
    # Delivery distance is 0, so no surcharge is applied.
    assert delivery_fee == DeliveryFee(delivery_fee=0)

    order_info = OrderInfo(
        cart_value=0,
        delivery_distance=1e3,
        number_of_items=0,
        time="2024-01-15T13:00:00Z"
    )
    delivery_fee = delivery_distance_fee.calculate(order_info)
    # Delivery distance is 1km, so surcharge is applied.
    assert delivery_fee == DeliveryFee(delivery_fee=2e2)

    order_info = OrderInfo(
        cart_value=0,
        delivery_distance=1.5e3,
        number_of_items=0,
        time="2024-01-15T13:00:00Z"
    )
    delivery_fee = delivery_distance_fee.calculate(order_info)
    # Delivery distance is 1.5km, so surcharge is applied.
    assert delivery_fee == DeliveryFee(delivery_fee=3e2)

    order_info = OrderInfo(
        cart_value=0,
        delivery_distance=2e3,
        number_of_items=0,
        time="2024-01-15T13:00:00Z"
    )

    delivery_distance_fee = DeliveryDistanceFee()
    delivery_fee = delivery_distance_fee.calculate(order_info)

    assert delivery_fee == DeliveryFee(delivery_fee=4e2)

    order_info = OrderInfo(
        cart_value=0,
        delivery_distance=2.5e3,
        number_of_items=0,
        time="2024-01-15T13:00:00Z"
    )

    delivery_distance_fee = DeliveryDistanceFee()
    delivery_fee = delivery_distance_fee.calculate(order_info)

    assert delivery_fee == DeliveryFee(delivery_fee=5e2)


def test__number_of_items_fee():
    number_of_items_fee = NumberOfItemsFee()
    order_info = OrderInfo(
        cart_value=0,
        delivery_distance=0,
        number_of_items=0,
        time="2024-01-15T13:00:00Z"
    )
    delivery_fee = number_of_items_fee.calculate(order_info)
    # Number of items is 0, so no surcharge is applied.
    assert delivery_fee == DeliveryFee(delivery_fee=0)

    order_info = OrderInfo(
        cart_value=0,
        delivery_distance=0,
        number_of_items=4,
        time="2024-01-15T13:00:00Z"
    )
    delivery_fee = number_of_items_fee.calculate(order_info)
    # Number of items is 4, so no surcharge is applied.
    assert delivery_fee == DeliveryFee(delivery_fee=0)

    order_info = OrderInfo(
        cart_value=0,
        delivery_distance=0,
        number_of_items=5,
        time="2024-01-15T13:00:00Z"
    )
    delivery_fee = number_of_items_fee.calculate(order_info)
    # Number of items is 5, so surcharge is applied.
    assert delivery_fee == DeliveryFee(delivery_fee=50)

    order_info = OrderInfo(
        cart_value=0,
        delivery_distance=0,
        number_of_items=10,
        time="2024-01-15T13:00:00Z"
    )
    delivery_fee = number_of_items_fee.calculate(order_info)
    # Number of items is 10, so surcharge is applied.
    assert delivery_fee == DeliveryFee(delivery_fee=3e2)

    order_info = OrderInfo(
        cart_value=0,
        delivery_distance=0,
        number_of_items=12,
        time="2024-01-15T13:00:00Z"
    )
    delivery_fee = number_of_items_fee.calculate(order_info)
    # Number of items is 12, so surcharge is applied. Bulk charge
    # is not applied since number of items is not greater than 12.
    assert delivery_fee == DeliveryFee(delivery_fee=4e2)

    order_info = OrderInfo(
        cart_value=0,
        delivery_distance=0,
        number_of_items=13,
        time="2024-01-15T13:00:00Z"
    )
    delivery_fee = number_of_items_fee.calculate(order_info)
    # Number of items is 13, so surcharge is applied. Bulk charge
    # is applied since number of items is greater than 12.
    assert delivery_fee == DeliveryFee(delivery_fee=9*50 + 1.2e2)

    order_info = OrderInfo(
        cart_value=0,
        delivery_distance=0,
        number_of_items=14,
        time="2024-01-15T13:00:00Z"
    )
    delivery_fee = number_of_items_fee.calculate(order_info)
    # Number of items is 14, so surcharge is applied. Bulk charge
    # is applied since number of items is greater than 12.
    assert delivery_fee == DeliveryFee(delivery_fee=(10*50) + 1.2e2)
