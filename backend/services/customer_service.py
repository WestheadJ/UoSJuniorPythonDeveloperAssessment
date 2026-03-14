# services/customer_service.py

from fastapi import HTTPException
from ..dal.customers import (
    get_customer_orders,
    get_active_customer_orders,
    get_active_customer_orders_with_pd,
)
import pandas as pd


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


def fetch_active_customer_orders() -> list:
    rows = get_active_customer_orders()

    if not rows:
        raise HTTPException(status_code=404, detail="No orders for active customers")

    else:
        return rows


def transform_customer_summary(df: pd.DataFrame) -> pd.DataFrame:
    """Aggregate order data to produce per-customer summary."""

    if df.empty:
        return df

    summary = (
        df.groupby(["customer_id", "name", "email", "customer_status"])
        .agg(
            total_spent=("order_total", "sum"),
            order_count=("order_id", "count"),
            items_purchased=("quantity", "sum"),
        )
        .reset_index()
    )

    return summary


def fetch_active_customer_orders_summary():
    rows = transform_customer_summary(get_active_customer_orders_with_pd())
    if rows.empty:
        raise HTTPException(status_code=404, detail="No orders for active customers")

    else:
        return rows.to_dict(orient="records")


def fetch_active_customer_orders_details():
    df = get_active_customer_orders_with_pd()

    if df.empty:
        return []

    return_data = []

    grouped = df.groupby("customer_id")

    for customer_id, group in grouped:

        first_row = group.iloc[0]
        selected_cols = group[
            ["order_id", "product", "unit_price", "quantity", "order_total"]
        ]
        orders_df = pd.DataFrame(selected_cols)
        # 3. Format the nested orders
        # We filter the columns we want and rename them to match your requirement
        orders_list = orders_df.rename(
            columns={"product": "product_name", "quantity": "amount"}
        ).to_dict(orient="records")

        # 4. Construct the dictionary
        customer_entry = {
            "customer_id": int(first_row["customer_id"]),  # Cast to int to be safe
            "name": str(first_row["name"]),
            "email": str(first_row["email"]),
            "order_total": float(group["order_total"].sum()),
            "orders": orders_list,
        }

        return_data.append(customer_entry)

    return return_data
