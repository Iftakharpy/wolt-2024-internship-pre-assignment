from abc import ABC, abstractmethod
from .models import OrderInfo, DeliveryFee
from copy import deepcopy
from pandas import Timestamp
from datetime import time


class DeliveryFeeTransformer(ABC):
    """Abstract class for all the fee transformers. 
    This class is used to transform the delivery fee after 
    the delivery fee has been calculated. So any subclass of this class
    is essentially one of the rules to transform the delivery fee."""

    @classmethod
    @abstractmethod
    def transform(self, delivery_info: OrderInfo, delivery_fee: DeliveryFee) -> DeliveryFee:
        """Transform the delivery fee."""


class FridayRushHourFeeTransformer(DeliveryFeeTransformer):
    """Transforms the delivery fee base don the following:
    During the Friday rush, 3 - 7 PM, the delivery fee (the 
    total fee including possible surcharges) will be multiplied 
    by 1.2x. Friday rush is 3 - 7 PM UTC."""

    @classmethod
    def transform(self, delivery_info: OrderInfo, delivery_fee: DeliveryFee) -> DeliveryFee:
        timestamp = Timestamp(delivery_info.delivery_time)
        transformed_delivery_fee = deepcopy(delivery_fee)

        rush_day = "Friday"
        rush_hour_start = time(hour=12+3, minute=0)  # 3:00:00 PM
        # 7:59:59.999999 PM
        rush_hour_end = time(hour=12+7, minute=59, second=59, microsecond=999999)
        rush_hour_fee_factor = 1.2  # 20% increase

        if (timestamp.day_name() == rush_day and
                (rush_hour_start <= timestamp.time() <= rush_hour_end)):
            transformed_delivery_fee *= rush_hour_fee_factor
        return transformed_delivery_fee


class LimitFeeTransformer(DeliveryFeeTransformer):
    """Transforms the delivery fee base don the following:
    The delivery fee can never be more than 15€, including possible surcharges."""
    @classmethod
    def transform(self, delivery_info: OrderInfo, delivery_fee: DeliveryFee) -> DeliveryFee:
        transformed_delivery_fee = deepcopy(delivery_fee)
        highest_limit_of_delivery_fee = 15e2  # 15€

        if transformed_delivery_fee > highest_limit_of_delivery_fee:
            transformed_delivery_fee = highest_limit_of_delivery_fee

        return transformed_delivery_fee


class ExcludeFeeTransformer(DeliveryFeeTransformer):
    """Transforms the delivery fee base don the following:
    The delivery is free (0€) when the cart value is equal or more than 200€."""
    @classmethod
    def transform(self, delivery_info: OrderInfo, delivery_fee: DeliveryFee) -> DeliveryFee:
        transformed_delivery_fee = deepcopy(delivery_fee)

        exclusion_cart_value_threshold = 200e2  # 200€
        exclusion_delivery_fee_factor = 1  # 100% decrease

        if delivery_info.cart_value >= exclusion_cart_value_threshold:
            transformed_delivery_fee -= (transformed_delivery_fee *
                                         exclusion_delivery_fee_factor)

        return transformed_delivery_fee


"""
In my opinion there should be another transformer that should check if the 
number of items are 0 and if so, set the delivery fee to 0. 
This would make sense since we are not delivering anything. so we should not 
charge anything.

Or perhaps, one transformer that checks if cart_value, delivery_distance and
number_of_items are 0 and if so, set the delivery fee to 0. Or throw error.
"""

# All fee transformers as singleton.
# Here order of the transformers matters.
ALL_FEE_TRANSFORMERS = [
    FridayRushHourFeeTransformer,
    LimitFeeTransformer,
    ExcludeFeeTransformer
]
