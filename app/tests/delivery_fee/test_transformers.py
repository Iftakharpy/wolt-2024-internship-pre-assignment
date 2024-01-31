from datetime import datetime
from app.delivery_fee.models import DeliveryFee, OrderInfo
from app.delivery_fee.fee_transformers import (
    FridayRushHourFeeTransformer,
    ExcludeFeeTransformer,
    LimitFeeTransformer,
)


def test__friday_rush_hour_fee_transformer():
    friday_rush_hour_fee_transformer = FridayRushHourFeeTransformer()
    order_info = OrderInfo(
        cart_value=0,
        delivery_distance=0,
        number_of_items=0,
        delivery_time="2024-01-15T13:00:00Z"
    )
    delivery_fee = friday_rush_hour_fee_transformer.transform(
        order_info,
        DeliveryFee(delivery_fee=0)
    )
    # Delivery time is not Friday rush hour, so no surcharge is applied.
    assert delivery_fee == DeliveryFee(delivery_fee=0)
