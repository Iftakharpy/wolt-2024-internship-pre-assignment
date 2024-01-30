from abc import ABC, abstractmethod
from .models import OrderInfo, DeliveryFee
from math import ceil


class DeliveryFeeCalculationStep(ABC):
    @abstractmethod
    def calculate(self, order_info: OrderInfo, delivery_fee_configs) -> DeliveryFee:
        """Calculate the delivery fee for the given order info."""


class CartValueFee(DeliveryFeeCalculationStep):
    def calculate(self, order_info: OrderInfo) -> DeliveryFee:
        delivery_fee = DeliveryFee(delivery_fee=0)
        cart_value_surcharge_threshold = 10e2  # 10€

        # Apply surcharge if cart value is less than 10€.
        if (order_info.cart_value < cart_value_surcharge_threshold):
            surcharge = cart_value_surcharge_threshold - order_info.cart_value
            delivery_fee += DeliveryFee(delivery_fee=surcharge)

        return delivery_fee


class DeliveryDistanceFee(DeliveryFeeCalculationStep):
    def calculate(self, order_info: OrderInfo) -> DeliveryFee:
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
    def calculate(self, order_info: OrderInfo) -> DeliveryFee:
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


ALL_CALCULATION_STEPS = [
    CartValueFee(),
    DeliveryDistanceFee(),
    NumberOfItemsFee(),
]
