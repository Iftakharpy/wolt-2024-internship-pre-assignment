from fastapi import APIRouter
from .models import OrderInfo, DeliveryFee

delivery_fee_router = APIRouter()


@delivery_fee_router.post("/calculate_delivery_fee/")
async def calculate_delivery_fee(order_info: OrderInfo) -> DeliveryFee:
    return DeliveryFee(delivery_fee=710)
