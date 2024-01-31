from app.delivery_fee.fee_calculation_steps import DeliveryFeeCalculationStep
from app.delivery_fee.fee_transformers import DeliveryFeeTransformer
from app.delivery_fee.models import OrderInfo, DeliveryFee
from app.delivery_fee.utility_meta_classes import ThreadSafeSingletonMeta
import app.delivery_fee.settings as settings


class DeliveryFeeCalculator(metaclass=ThreadSafeSingletonMeta):
    """Calculates delivery fee. This is singleton class. This means only the first
    instance of this class will be used throughout the application."""

    def __init__(self, calculation_steps: list[DeliveryFeeCalculationStep] | None = None,
                 transformers: list[DeliveryFeeTransformer] | None = None,
                 calculation_configurations: None = None):
        self.calculation_steps = calculation_steps
        if calculation_steps is None:
            self.calculation_steps = settings.ALL_CALCULATION_STEPS

        self.transformers = transformers
        if transformers is None:
            self.transformers = settings.ALL_FEE_TRANSFORMERS

        # This is a plan for future, so that parameters can be changed easily.
        # And may be in the future we can have different configurations for
        # different users depending on country, city, etc.
        self.calculation_configurations = calculation_configurations
        if calculation_configurations is None:
            self.calculation_configurations = None

    def calculate(self, order_info: OrderInfo) -> DeliveryFee:
        calculated_fee = DeliveryFee(delivery_fee=0)

        # Follow all the steps to calculate the delivery fee.
        for step in self.calculation_steps:
            calculated_fee += step.calculate(order_info)

        # Apply all the transformations to the calculated delivery fee.
        for transformer in self.transformers:
            calculated_fee = transformer.transform(order_info, calculated_fee)

        return calculated_fee


# Delivery calculator singleton.
DELIVERY_FEE_CALCULATOR = DeliveryFeeCalculator(
    settings.ALL_CALCULATION_STEPS, settings.ALL_FEE_TRANSFORMERS)
