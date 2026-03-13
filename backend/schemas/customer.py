from pydantic import BaseModel
from datetime import date
from typing import List


class OrderSchema(BaseModel):
    order_id: int
    product: str
    quantity: int
    unit_price: float
    order_date: date


class CustomerResponse(BaseModel):
    customer_id: int
    first_name: str
    last_name: str
    email: str
    customer_status: str
    orders: List[OrderSchema] = []
