from abc import ABC, abstractmethod
from app.delivery_fee.models import OrderInfo, DeliveryFee
from copy import deepcopy
from pandas import Timestamp
from datetime import time
from pydantic import BaseModel
from typing import Self


class DeliveryFeeTransformer(ABC):
    """Abstract class for all the fee transformers. 
    This class is used to transform the delivery fee after 
    the delivery fee has been calculated. So any subclass of this class
    is essentially one of the rules to transform the delivery fee."""

    class ConfigOptions(BaseModel):
        """Configuration options for DeliveryFeeTransformer."""

    @abstractmethod
    def transform(self, delivery_info: OrderInfo, delivery_fee: DeliveryFee) -> DeliveryFee:
        """Transform the delivery fee."""


class RushHourFeeTransformer(DeliveryFeeTransformer):
    """Transforms the delivery fee base don the following:
    During the Friday rush, 3 - 7 PM, the delivery fee (the 
    total fee including possible surcharges) will be multiplied 
    by 1.2x. Friday rush is 3 - 7 PM UTC."""

    class ConfigOptions(BaseModel):
        """Configuration options for RushHourFeeTransformer.

        Default for Friday rush hour from 3:00:00 PM to 7:59:59.999999 PM UTC.
        >>> from datetime import time
        >>> rush_day: str = "Friday"
        >>> rush_hour_start: time = time(hour=12+3, minute=0)  # 3:00:00 PM (inclusive)
        >>> # 7:59:59.999999 PM (inclusive)
        >>> rush_hour_end: time = time(hour=12+7, minute=59, second=59, microsecond=999999)
        >>> rush_hour_fee_factor: float = 1.2  # 20% increase
        """
        rush_day: str = "Friday"
        rush_hour_start: time = time(hour=12+3, minute=0)  # 3:00:00 PM
        # 7:59:59.999999 PM
        rush_hour_end: time = time(hour=12+7, minute=59, second=59, microsecond=999999)
        rush_hour_fee_factor: float = 1.2  # 20% increase

    def __init__(self, config_options: ConfigOptions | None = None) -> None:
        super().__init__()
        self.config_options = config_options
        if config_options is None:
            self.config_options = self.ConfigOptions()

    def transform(self, delivery_info: OrderInfo, delivery_fee: DeliveryFee) -> DeliveryFee:
        timestamp = Timestamp(delivery_info.time)
        transformed_delivery_fee = deepcopy(delivery_fee)

        if (timestamp.day_name() == self.config_options.rush_day and
                (self.config_options.rush_hour_start <= timestamp.time() <= self.config_options.rush_hour_end)):
            transformed_delivery_fee *= self.config_options.rush_hour_fee_factor

        return transformed_delivery_fee


class LimitFeeTransformer(DeliveryFeeTransformer):
    """Transforms the delivery fee base don the following:
    The delivery fee can never be more than 15€, including possible surcharges."""

    class ConfigOptions(BaseModel):
        """Configuration options for LimitFeeTransformer.

        Default options are:
        >>> highest_limit_of_delivery_fee = 15e2  # 15€ (inclusive)
        """
        highest_limit_of_delivery_fee: int = 15e2

    def __init__(self, config_options: ConfigOptions | None = None) -> None:
        super().__init__()
        self.config_options = config_options
        if config_options is None:
            self.config_options = self.ConfigOptions()

    def transform(self, delivery_info: OrderInfo, delivery_fee: DeliveryFee) -> DeliveryFee:
        transformed_delivery_fee = deepcopy(delivery_fee)

        if transformed_delivery_fee >= self.config_options.highest_limit_of_delivery_fee:
            transformed_delivery_fee = DeliveryFee(
                delivery_fee=self.config_options.highest_limit_of_delivery_fee)

        return transformed_delivery_fee


class ReduceFeeTransformer(DeliveryFeeTransformer):
    """Transforms the delivery fee base don the following:
    The delivery is free (0€) when the cart value is equal or more than 200€."""

    class ConfigOptions(BaseModel):
        """Configuration options for ExcludeFeeTransformer.

        Default options are:
        >>> exclusion_cart_value_threshold = 200e2  # 200€ (inclusive)
        >>> exclusion_delivery_fee_factor = 1  # 100% decrease
        """
        exclusion_cart_value_threshold: int = 200e2
        exclusion_delivery_fee_factor: float = 1

    def __init__(self, config_options: ConfigOptions | None = None) -> None:
        super().__init__()
        self.config_options = config_options
        if config_options is None:
            self.config_options = self.ConfigOptions()

    def transform(self, delivery_info: OrderInfo, delivery_fee: DeliveryFee) -> DeliveryFee:
        transformed_delivery_fee = deepcopy(delivery_fee)

        if delivery_info.cart_value >= self.config_options.exclusion_cart_value_threshold:
            transformed_delivery_fee -= (transformed_delivery_fee *
                                         self.config_options.exclusion_delivery_fee_factor)

        return transformed_delivery_fee


"""
In my opinion there should be another transformer that should check if the 
number of items are 0 and if so, set the delivery fee to 0. 
This would make sense since we are not delivering anything. so we should not 
charge anything.

Or perhaps, one transformer that checks if cart_value, delivery_distance and
number_of_items are 0 and if so, set the delivery fee to 0. Or throw error.
"""
