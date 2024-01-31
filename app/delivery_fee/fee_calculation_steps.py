from abc import ABC, abstractmethod
from app.delivery_fee.models import OrderInfo, DeliveryFee
from math import ceil


class DeliveryFeeCalculationStep(ABC):
    """Abstract class for all the calculation steps. 
    These steps are used to calculate the delivery fee. 
    Any subclass of this class is essentially one of the rules 
    to calculate surcharge for the total delivery fee."""

    @classmethod
    @abstractmethod
    def calculate(cls, order_info: OrderInfo, delivery_fee_configs) -> DeliveryFee:
        """Calculate the delivery fee for the given order info."""


class CartValueFee(DeliveryFeeCalculationStep):
    """Calculates delivery fee on cart value with the following rule:
    If the cart value is less than 10€, a small order surcharge is added to 
    the delivery price. The surcharge is the difference between the cart value 
    and 10€. For example if the cart value is 8.90€, the surcharge will be 1.10€."""

    @classmethod
    def calculate(cls, order_info: OrderInfo) -> DeliveryFee:
        delivery_fee = DeliveryFee(delivery_fee=0)
        cart_value_surcharge_threshold = 10e2  # 10€

        # Apply surcharge if cart value is less than 10€.
        if (order_info.cart_value < cart_value_surcharge_threshold):
            surcharge = cart_value_surcharge_threshold - order_info.cart_value
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

    @classmethod
    def calculate(cls, order_info: OrderInfo) -> DeliveryFee:
        delivery_fee = DeliveryFee(delivery_fee=0)

        delivery_distance_low_threshold = 1e3  # 1km
        delivery_distance_surcharge_for_low_threshold = 2e2  # 2€
        additional_fee = 1e2  # 1€
        additional_fee_applied_per_meters_traveled = 500  # 500m

        # Apply surcharge for first 1km.
        if order_info.delivery_distance > 0:
            delivery_fee += delivery_distance_surcharge_for_low_threshold

        # Apply additional fee for every 500m traveled.
        if order_info.delivery_distance > delivery_distance_low_threshold:
            additional_fee_multiplier = ceil((
                order_info.delivery_distance - delivery_distance_low_threshold
            ) / additional_fee_applied_per_meters_traveled)

            delivery_fee += (additional_fee_multiplier * additional_fee)

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

    @classmethod
    def calculate(cls, order_info: OrderInfo) -> DeliveryFee:
        delivery_fee = DeliveryFee(delivery_fee=0)

        number_of_items_surcharge_threshold = 4  # 4 items
        surcharge_per_item_over_threshold = 50  # 50 cents
        bulk_charge = 1.2e2  # 1.20€
        bulk_charge_threshold = 12

        # Apply surcharge if number of items is more than the threshold.
        if order_info.number_of_items > number_of_items_surcharge_threshold:
            surcharge = (
                order_info.number_of_items - number_of_items_surcharge_threshold
            ) * surcharge_per_item_over_threshold

            delivery_fee += surcharge

        # Apply bulk charge for items.
        if order_info.number_of_items > bulk_charge_threshold:
            delivery_fee += bulk_charge

        return delivery_fee


# All the calculation steps as singleton.
# Here order of the calculation steps does not matters.
ALL_CALCULATION_STEPS = [
    CartValueFee,
    DeliveryDistanceFee,
    NumberOfItemsFee,
]
