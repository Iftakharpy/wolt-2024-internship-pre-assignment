from fastapi import APIRouter
from .models import OrderInfo, DeliveryFee
from .fee_calculator import DELIVERY_FEE_CALCULATOR

delivery_fee_router = APIRouter()


@delivery_fee_router.post("/calculate_delivery_fee/")
async def calculate_delivery_fee(order_info: OrderInfo) -> DeliveryFee:
    return DELIVERY_FEE_CALCULATOR.calculate(order_info)
