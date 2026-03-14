# api/customers.py

from fastapi import APIRouter
from ..services.customer_service import (
    fetch_customer_orders,
    fetch_active_customer_orders,
    fetch_active_customer_orders_summary,
    fetch_active_customer_orders_details,
)
import json

router = APIRouter(prefix="/customers", tags=["customers"])


@router.get("/{customer_id}/orders")
def get_customer_orders(customer_id: int):
    return fetch_customer_orders(customer_id)


@router.get("/active/orders")
def get_active_customer_orders():
    return fetch_active_customer_orders()


@router.get("/active/orders/summary")
def get_active_customer_orders_summary():
    return fetch_active_customer_orders_summary()


@router.get("/active/orders/details")
def get_active_customer_orders_detail():
    return fetch_active_customer_orders_details()
