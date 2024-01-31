from app.delivery_fee.fee_calculation_steps import ALL_CALCULATION_STEPS
from app.delivery_fee.fee_transformers import ALL_FEE_TRANSFORMERS
from app.delivery_fee.fee_calculator import DeliveryFeeCalculator


def test__initialize_delivery_fee_calculator_with_default_params():
    delivery_fee_calculator = DeliveryFeeCalculator()
    assert delivery_fee_calculator.calculation_steps == ALL_CALCULATION_STEPS
    assert delivery_fee_calculator.transformers == ALL_FEE_TRANSFORMERS


def test__initialize_delivery_fee_calculator_with_None():
    delivery_fee_calculator = DeliveryFeeCalculator(None, None)
    assert delivery_fee_calculator.calculation_steps == ALL_CALCULATION_STEPS
    assert delivery_fee_calculator.transformers == ALL_FEE_TRANSFORMERS


def test__initialization_delivery_fee_with_params():
    DeliveryFeeCalculator.clear_singleton_instance()
    calc_steps = [ALL_CALCULATION_STEPS[0]]
    transformers = [ALL_FEE_TRANSFORMERS[0]]
    delivery_fee_calculator = DeliveryFeeCalculator(
        calculation_steps=calc_steps, transformers=transformers)
    assert delivery_fee_calculator.calculation_steps == calc_steps
    assert delivery_fee_calculator.transformers == transformers
