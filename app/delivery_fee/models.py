from typing import Annotated, Self
from pydantic import BaseModel, field_validator
from datetime import datetime


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

    @field_validator('cart_value')
    def cart_value__must_be_non_negative(cls, value):
        if value < 0:
            raise ValueError('cart_value must be non-negative')
        return value

    @field_validator('delivery_distance')
    def delivery_distance__must_be_non_negative(cls, value):
        if value < 0:
            raise ValueError('delivery_distance must be non-negative')
        return value

    @field_validator('number_of_items')
    def number_of_items__must_be_non_negative(cls, value):
        if value < 0:
            raise ValueError('number_of_items must be non-negative')
        return value

    @field_validator('delivery_time', mode='before')
    def delivery_time__parser(cls, value):
        try:
            if isinstance(value, str):
                return datetime.fromisoformat(value)
            raise ValueError
        except ValueError:
            raise ValueError(
                'delivery_time must be in UTC ISO format (e.g. 2024-01-15T13:00:00Z)')


class DeliveryFee(BaseModel):
    # in cents (e.g. €1.00 = 100 = 1e2)
    delivery_fee: Annotated[int,
                            ("Calculated delivery fee in cents. "
                             "Example: 710 (710 cents = 7.10€)")]

    @field_validator('delivery_fee')
    def delivery_fee__must_be_non_negative(cls, value):
        if value < 0:
            raise ValueError('delivery_fee must be non-negative')
        return value

    def __sub__(self, other: Self | int | float) -> Self:
        if isinstance(other, (int, float)):
            total_fee = max(self.delivery_fee - other, 0)
        elif isinstance(other, DeliveryFee):
            total_fee = max(self.delivery_fee - other.delivery_fee, 0)
        else:
            raise TypeError(
                f"Unsupported operand type(s) for -: '{type(self)}' and '{type(other)}'")
        return DeliveryFee(delivery_fee=total_fee)

    def __add__(self, other: Self | int | float) -> Self:
        if isinstance(other, (int, float)):
            total_fee = max(self.delivery_fee + other, 0)
        elif isinstance(other, DeliveryFee):
            total_fee = max(self.delivery_fee + other.delivery_fee, 0)
        else:
            raise TypeError(
                f"Unsupported operand type(s) for +: '{type(self)}' and '{type(other)}'")
        return DeliveryFee(delivery_fee=total_fee)

    def __mul__(self, other: int | float) -> Self:
        if not isinstance(other, (int, float)):
            raise TypeError(
                f"Unsupported operand type(s) for *: '{type(self)}' and '{type(other)}'")
        total_fee = max(self.delivery_fee * other, 0)
        return DeliveryFee(delivery_fee=total_fee)

    def __div__(self, other: int | float) -> Self:
        if not isinstance(other, (int, float)):
            raise TypeError(
                f"Unsupported operand type(s) for /: '{type(self)}' and '{type(other)}'")
        total_fee = max(self.delivery_fee / other, 0)
        return DeliveryFee(delivery_fee=total_fee)

    def __gt__(self, other: Self | int | float) -> bool:
        if isinstance(other, (int, float)):
            return self.delivery_fee > other
        elif isinstance(other, DeliveryFee):
            return self.delivery_fee > other.delivery_fee
        else:
            raise TypeError(
                f"Unsupported operand type(s) for >: '{type(self)}' and '{type(other)}'")

    def __lt__(self, other: Self | int | float) -> bool:
        if isinstance(other, (int, float)):
            return self.delivery_fee < other
        elif isinstance(other, DeliveryFee):
            return self.delivery_fee < other.delivery_fee
        else:
            raise TypeError(
                f"Unsupported operand type(s) for <: '{type(self)}' and '{type(other)}'")

    def __eq__(self, other: Self | int | float) -> bool:
        if isinstance(other, (int, float)):
            return self.delivery_fee == other
        elif isinstance(other, DeliveryFee):
            return self.delivery_fee == other.delivery_fee
        else:
            raise TypeError(
                f"Unsupported operand type(s) for ==: '{type(self)}' and '{type(other)}'")
