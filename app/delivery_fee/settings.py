"""
This module contains all the configuration for the delivery fee.
"""
from datetime import time
from app.delivery_fee.fee_calculation_steps import (
    CartValueFee,
    DeliveryDistanceFee,
    NumberOfItemsFee,
)
from app.delivery_fee.fee_transformers import (
    FridayRushHourFeeTransformer,
    ExcludeFeeTransformer,
    LimitFeeTransformer,
)


#########################################################################################
# Fee Calculation Steps
#########################################################################################

# Settings for fee calculation steps.
CART_VALUE_CONFIG_OPTIONS = CartValueFee.ConfigOptions(
    cart_value_surcharge_threshold=10e2,  # 50€ (inclusive)
)
DELIVERY_DISTANCE_CONFIG_OPTIONS = DeliveryDistanceFee.ConfigOptions(
    delivery_distance_low_threshold=1e3,  # 1km (inclusive)
    delivery_distance_surcharge_for_low_threshold=2e2,  # 2€
    additional_fee=1e2,  # 1€
    additional_fee_applied_per_meters_traveled=500,  # 500m (inclusive)
)
NUMBER_OF_ITEMS_CONFIG_OPTIONS = NumberOfItemsFee.ConfigOptions(
    number_of_items_surcharge_threshold=10,  # 10 items (inclusive)
    surcharge_per_item_over_threshold=5e2,  # 5€
    bulk_charge=12,  # 12 items (inclusive)
    bulk_charge_threshold=1.2e2,  # 1.20€
)


# Here order of the calculation steps does not matters.
ALL_CALCULATION_STEPS = [
    CartValueFee(CART_VALUE_CONFIG_OPTIONS),
    DeliveryDistanceFee(DELIVERY_DISTANCE_CONFIG_OPTIONS),
    NumberOfItemsFee(NUMBER_OF_ITEMS_CONFIG_OPTIONS),
]


#########################################################################################
# Transformation Steps
#########################################################################################

# Settings for fee transformers.
FRIDAY_RUSH_HOUR_CONFIG_OPTIONS = FridayRushHourFeeTransformer.ConfigOptions(
    rush_day="Friday",
    rush_hour_start=time(hour=12+3, minute=0),  # 3:00:00 PM (inclusive)
    rush_hour_end=time(hour=12+7, minute=59, second=59,
                       microsecond=999999),  # 7:59:59.999999 PM (inclusive)
    rush_hour_fee_factor=1.2,  # 20% increase
)
LIMIT_FEE_CONFIG_OPTIONS = LimitFeeTransformer.ConfigOptions(
    highest_limit_of_delivery_fee=15e2,  # 15€ (exclusive)
)

EXCLUDE_FEE_CONFIG_OPTIONS = ExcludeFeeTransformer.ConfigOptions(
    exclusion_cart_value_threshold=200e2,  # 200€ (inclusive)
    exclusion_delivery_fee_factor=1,  # 100% (decrease)
)


# Here order of the transformers matters.
ALL_FEE_TRANSFORMERS = [
    FridayRushHourFeeTransformer(),
    LimitFeeTransformer(),
    ExcludeFeeTransformer()
]
