from .fee_calculation_steps import ALL_CALCULATION_STEPS, DeliveryFeeCalculationStep
from .fee_transformers import ALL_FEE_TRANSFORMERS, DeliveryFeeTransformer
from .models import OrderInfo, DeliveryFee


class DeliveryFeeCalculator:
    def __init__(self, delivery_fee_calculation_steps: list[DeliveryFeeCalculationStep] = ALL_CALCULATION_STEPS,
                 delivery_fee_transformers: list[DeliveryFeeTransformer] = ALL_FEE_TRANSFORMERS,
                 delivery_fee_calculation_configurations: None = None):
        self.delivery_fee_calculation_steps = delivery_fee_calculation_steps
        self.delivery_fee_transformers = delivery_fee_transformers
        # Thi is a plan for future, so that parameters can be changed dynamically.
        self.delivery_fee_calculation_configurations = delivery_fee_calculation_configurations

    def calculate(self, order_info: OrderInfo) -> DeliveryFee:
        calculated_fee = DeliveryFee(delivery_fee=0)

        # Follow all the steps to calculate the delivery fee.
        for step in self.delivery_fee_calculation_steps:
            calculated_fee += step.calculate(order_info)

        # Apply all the transformations to the calculated delivery fee.
        for transformer in self.delivery_fee_transformers:
            calculated_fee = transformer.transform(order_info, calculated_fee)

        return calculated_fee


DELIVERY_FEE_CALCULATOR = DeliveryFeeCalculator()
