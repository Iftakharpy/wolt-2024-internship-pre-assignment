from typing import Annotated
from fastapi import FastAPI
from pydantic import BaseModel
from datetime import datetime


app = FastAPI()


class OrderInfo(BaseModel):
    # in cents (e.g. €1.00 = 100 = 1e2)
    cart_value: Annotated[int,
                          ("Value of the shopping cart in cents. "
                           "Example: 790 (790 cents = 7.90€)")]
    # in meters (e.g. 1km = 1000 = 1e3)
    delivery_distance: Annotated[int,
                                 ("The distance between the store and customer’s "
                                  "location in meters. Example: 2235 (2235 meters "
                                  "= 2.235 km)")]
    number_of_items: Annotated[int,
                               ("The number of items in the customer's shopping cart. "
                                "Example: 4 (customer has 4 items in the cart)")]
    # timestamp in UTC ISO format (e.g. 2024-01-15T13:00:00Z)
    delivery_time: Annotated[datetime,
                             ("Order time in UTC in ISO format. "
                              "Example: 2024-01-15T13:00:00Z")]


class DeliveryFee(BaseModel):
    # in cents (e.g. €1.00 = 100 = 1e2)
    delivery_fee: Annotated[int,
                            ("Calculated delivery fee in cents. "
                             "Example: 710 (710 cents = 7.10€)")]


@app.post("/calculate_delivery_fee/")
async def calculate_delivery_fee(order_info: OrderInfo) -> DeliveryFee:
    return DeliveryFee(delivery_fee=710)
