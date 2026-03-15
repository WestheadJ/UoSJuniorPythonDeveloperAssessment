# api/customers.py

from fastapi import APIRouter  # type: ignore
from ..services.orders_service import (
    fetch_active_customer_orders,
    fetch_active_customer_orders_summary,
    fetch_active_customer_orders_details,
)

router = APIRouter(prefix="/orders", tags=["orders"])


@router.get("/active/customers")
def get_active_customer_orders():
    return fetch_active_customer_orders()


@router.get("/active/customers/summary")
def get_active_customer_orders_summary():
    return fetch_active_customer_orders_summary()


@router.get("/active/customers/details")
def get_active_customer_orders_detail():
    return fetch_active_customer_orders_details()
