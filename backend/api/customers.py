# api/customers.py

from fastapi import APIRouter
from ..services.customer_service import fetch_customer_orders

router = APIRouter(prefix="/customers", tags=["customers"])


@router.get("/{customer_id}/orders")
def get_customer_orders(customer_id: int):
    return fetch_customer_orders(customer_id)
