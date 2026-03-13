# services/customer_service.py

from fastapi import HTTPException
from ..dal.customers import get_customer_orders


def fetch_customer_orders(customer_id: int):
    rows = get_customer_orders(customer_id)

    if not rows:
        raise HTTPException(status_code=404, detail="Customer not found")

    first_row = rows[0]

    customer = {
        "customer_id": first_row["customer_id"],
        "first_name": first_row["first_name"],
        "last_name": first_row["last_name"],
        "email": first_row["email"],
        "customer_status": first_row["customer_status"],
        "orders": [],
    }

    for row in rows:
        if row["order_id"] is not None:
            customer["orders"].append(
                {
                    "order_id": row["order_id"],
                    "product": row["product"],
                    "quantity": row["quantity"],
                    "unit_price": row["unit_price"],
                    "order_date": row["order_date"],
                }
            )

    return customer
