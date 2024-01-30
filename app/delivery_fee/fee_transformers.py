from abc import ABC, abstractmethod
from .models import OrderInfo, DeliveryFee
from copy import deepcopy
from pandas import Timestamp


class DeliveryFeeTransformer(ABC):
    @abstractmethod
    def transform(self, delivery_info: OrderInfo, delivery_fee: DeliveryFee) -> DeliveryFee:
        """Transform the delivery fee."""


class FridayRushHourFeeTransformer(DeliveryFeeTransformer):
    def transform(self, delivery_info: OrderInfo, delivery_fee: DeliveryFee) -> DeliveryFee:
        transformed_delivery_fee = deepcopy(delivery_fee)
        rush_day = "Friday"
        rush_hour_start = 12 + 3    # 3pm
        rush_hour_end = 12 + 7      # 7pm
        rush_hour_factor = 1.2      # 20% increase
        timestamp = Timestamp(delivery_info.delivery_time)

        if (timestamp.day_name() == rush_day and
                (rush_hour_start <= timestamp.hour <= rush_hour_end)):
            transformed_delivery_fee *= rush_hour_factor
        return transformed_delivery_fee


class LimitFeeTransformer(DeliveryFeeTransformer):
    def transform(self, delivery_info: OrderInfo, delivery_fee: DeliveryFee) -> DeliveryFee:
        transformed_delivery_fee = deepcopy(delivery_fee)
        highest_limit_of_delivery_fee = 15e2  # 15€

        if transformed_delivery_fee > highest_limit_of_delivery_fee:
            transformed_delivery_fee = highest_limit_of_delivery_fee

        return transformed_delivery_fee


class ExcludeFeeTransformer(DeliveryFeeTransformer):
    def transform(self, delivery_info: OrderInfo, delivery_fee: DeliveryFee) -> DeliveryFee:
        transformed_delivery_fee = deepcopy(delivery_fee)

        exclusion_cart_value_threshold = 200e2  # 200€
        exclude_delivery_fee_factor = 1  # 100% decrease

        if delivery_info.cart_value >= exclusion_cart_value_threshold:
            transformed_delivery_fee -= (transformed_delivery_fee *
                                         exclude_delivery_fee_factor)

        return transformed_delivery_fee


"""
In my opinion there should be another transformer that should check if the 
number of items are 0 and if so, set the delivery fee to 0. 
This would make sense since we are not delivering anything. so we should not 
charge anything.

Or perhaps, one transformer that checks if cart_value, delivery_distance and
number_of_items are 0 and if so, set the delivery fee to 0. Or throw error.
"""


ALL_FEE_TRANSFORMERS = [
    FridayRushHourFeeTransformer(),
    LimitFeeTransformer(),
    ExcludeFeeTransformer()
]
