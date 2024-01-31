from fastapi import APIRouter
from .models import OrderInfo, DeliveryFee
from .fee_calculator import DELIVERY_FEE_CALCULATOR

delivery_fee_router = APIRouter()


@delivery_fee_router.post("/calculate_delivery_fee/")
async def calculate_delivery_fee(order_info: OrderInfo) -> DeliveryFee:
    return DELIVERY_FEE_CALCULATOR.calculate(order_info)


"""
Maybe in future we can add different rates for different countries.
"""
# @delivery_fee_router.post("/calculate_delivery_fee/fi/")
# async def calculate_delivery_fee_for_finland(order_info: OrderInfo) -> DeliveryFee:
#     return DELIVERY_FEE_CALCULATOR.calculate(order_info, locale="fi")


# @delivery_fee_router.post("/calculate_delivery_fee/de/")
# async def calculate_delivery_fee_for_germany(order_info: OrderInfo) -> DeliveryFee:
#     return DELIVERY_FEE_CALCULATOR.calculate(order_info, locale="fi")
