from abc import ABC, abstractmethod
from app.delivery_fee.models import OrderInfo, DeliveryFee
from pydantic import BaseModel
from math import ceil


class DeliveryFeeCalculationStep(ABC):
    """Abstract class for all the calculation steps. 
    These steps are used to calculate the delivery fee. 
    Any subclass of this class is essentially one of the rules 
    to calculate surcharge for the total delivery fee."""

    class ConfigOptions(BaseModel):
        """Configuration options for DeliveryFeeTransformer."""

    @abstractmethod
    def calculate(cls, order_info: OrderInfo, delivery_fee_configs) -> DeliveryFee:
        """Calculate the delivery fee for the given order info."""


class CartValueFee(DeliveryFeeCalculationStep):
    """Calculates delivery fee on cart value with the following rule:
    If the cart value is less than 10€, a small order surcharge is added to 
    the delivery price. The surcharge is the difference between the cart value 
    and 10€. For example if the cart value is 8.90€, the surcharge will be 1.10€."""

    class ConfigOptions(BaseModel):
        """Configuration options for CartValueFee.

        Default for surcharge threshold is 10€.
        >>> cart_value_surcharge_threshold: int = 10e2  # 10€ (inclusive)
        """
        cart_value_surcharge_threshold: int = 10e2

    def __init__(self, config_options: ConfigOptions | None = None) -> None:
        super().__init__()
        self.config_options = config_options
        if config_options is None:
            self.config_options = self.ConfigOptions()

    def calculate(self, order_info: OrderInfo) -> DeliveryFee:
        delivery_fee = DeliveryFee(delivery_fee=0)

        # Apply surcharge if cart value is less than 10€.
        if (order_info.cart_value < self.config_options.cart_value_surcharge_threshold):
            surcharge = self.config_options.cart_value_surcharge_threshold - order_info.cart_value
            delivery_fee += DeliveryFee(delivery_fee=surcharge)

        return delivery_fee


class DeliveryDistanceFee(DeliveryFeeCalculationStep):
    """Calculates delivery fee on the delivery distance using the following rule:
    A delivery fee for the first 1000 meters (=1km) is 2€. If the delivery distance 
    is longer than that, 1€ is added for every additional 500 meters that the courier 
    needs to travel before reaching the destination. Even if the distance would be 
    shorter than 500 meters, the minimum fee is always 1€.

        Example 1: If the delivery distance is 1499 meters, 
            the delivery fee is: 2€ base fee + 1€ for the additional 500 m => 3€

        Example 2: If the delivery distance is 1500 meters, 
            the delivery fee is: 2€ base fee + 1€ for the additional 500 m => 3€

        Example 3: If the delivery distance is 1501 meters, 
            the delivery fee is: 2€ base fee + 1€ for the first 500 m + 1€ for the second 500 m => 4€
    """

    class ConfigOptions(BaseModel):
        """Configuration options for DeliveryDistanceFee.

        Default options are:
        >>> delivery_distance_low_threshold = 1e3  # 1km (inclusive)
        >>> delivery_distance_surcharge_for_low_threshold = 2e2  # 2€
        >>> additional_fee = 1e2  # 1€
        >>> additional_fee_applied_per_meters_traveled = 500  # 500m (inclusive)
        """
        delivery_distance_low_threshold: int = 1e3
        delivery_distance_surcharge_for_low_threshold: int = 2e2
        additional_fee: int = 1e2
        additional_fee_applied_per_meters_traveled: int = 500

    def __init__(self, config_options: ConfigOptions | None = None) -> None:
        super().__init__()
        self.config_options = config_options
        if config_options is None:
            self.config_options = self.ConfigOptions()

    def calculate(self, order_info: OrderInfo) -> DeliveryFee:
        delivery_fee = DeliveryFee(delivery_fee=0)

        # Apply surcharge for first 1km.
        if order_info.delivery_distance > 0:
            delivery_fee += self.config_options.delivery_distance_surcharge_for_low_threshold

        # Apply additional fee for every 500m traveled.
        if order_info.delivery_distance > self.config_options.delivery_distance_low_threshold:
            additional_fee_multiplier = ceil((
                order_info.delivery_distance - self.config_options.delivery_distance_low_threshold
            ) / self.config_options.additional_fee_applied_per_meters_traveled)

            delivery_fee += (additional_fee_multiplier *
                             self.config_options.additional_fee)

        return delivery_fee


class NumberOfItemsFee(DeliveryFeeCalculationStep):
    """Calculates delivery fee on number of items using the following rule:
    If the number of items is five or more, an additional 50 cent surcharge 
    is added for each item above and including the fifth item. An extra 
    "bulk" fee applies for more than 12 items of 1,20€

    Example 1: If the number of items is 4, no extra surcharge

    Example 2: If the number of items is 5, 50 cents surcharge is added

    Example 3: If the number of items is 10, 3€ surcharge (6 x 50 cents) is added

    Example 4: If the number of items is 13, 5,
        70€ surcharge is added ((9 * 50 cents) + 1,20€)

    Example 5: If the number of items is 14, 
        6,20€ surcharge is added ((10 * 50 cents) + 1,20€)"""

    class ConfigOptions(BaseModel):
        """Configuration options for NumberOfItemsFee.

        Default options are:
        >>> number_of_items_surcharge_threshold = 4  # 4 items (inclusive)
        >>> surcharge_per_item_over_threshold = 50  # 50 cents
        >>> bulk_charge = 1.2e2  # 1.20€
        >>> bulk_charge_threshold = 12 (exclusive)
        """
        number_of_items_surcharge_threshold: int = 4
        surcharge_per_item_over_threshold: int = 50
        bulk_charge: int = 1.2e2
        bulk_charge_threshold: int = 12

    def __init__(self, config_options: ConfigOptions | None = None) -> None:
        super().__init__()
        self.config_options = config_options
        if config_options is None:
            self.config_options = self.ConfigOptions()

    def calculate(self, order_info: OrderInfo) -> DeliveryFee:
        delivery_fee = DeliveryFee(delivery_fee=0)

        # Apply surcharge if number of items is more than the threshold.
        if order_info.number_of_items > self.config_options.number_of_items_surcharge_threshold:
            surcharge = (
                order_info.number_of_items - self.config_options.number_of_items_surcharge_threshold
            ) * self.config_options.surcharge_per_item_over_threshold

            delivery_fee += surcharge

        # Apply bulk charge for items.
        if order_info.number_of_items > self.config_options.bulk_charge_threshold:
            delivery_fee += self.config_options.bulk_charge

        return delivery_fee
