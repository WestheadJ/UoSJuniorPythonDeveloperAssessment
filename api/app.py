from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List
from .db import get_db_conn  # Importing your context manager

app = FastAPI(title="Junior Developer Assessment API")


class OrderSchema(BaseModel):
    order_id: int
    product: str
    quantity: int
    unit_price: float
    customer_status: str
    order_date: str


class CustomerResponse(BaseModel):
    customer_id: int
    first_name: str
    last_name: str
    email: str

    orders: List[OrderSchema]


@app.get("/health")
def health_check():
    """
    Endpoint to verify API and database health.
    """
    try:
        with get_db_conn() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT name FROM sqlite_master WHERE type='table' AND name='Customers';"
            )

            if not cursor.fetchone():
                return {
                    "status": "unhealthy",
                    "detail": "Database is connected but schema is missing. Run bootstrap script.",
                }

        return {"status": "healthy"}
    except Exception as e:
        return {"status": "unhealthy", "detail": str(e)}


@app.get("/customers/{customer_id}/orders", response_model=CustomerResponse)
def get_customer_orders(customer_id: int):
    with get_db_conn() as CON:
        cursor = CON.cursor()

        query = """
            SELECT 
                c.customer_id, c.first_name, c.last_name, c.email, c.customer_status,
                o.order_id, o.product, o.quantity, o.unit_price, o.order_date
            FROM Customers c
            LEFT JOIN Orders o ON c.customer_id = o.customer_id
            WHERE c.customer_id = ?
        """
        cursor.execute(query, (customer_id,))
        rows = cursor.fetchall()

        if not rows:
            raise HTTPException(status_code=404, detail="Customer not found")

        first_row = rows[0]
        customer_data = {
            "customer_id": first_row["customer_id"],
            "first_name": first_row["first_name"],
            "last_name": first_row["last_name"],
            "email": first_row["email"],
            "customer_status": first_row["customer_status"],
            "orders": [],
        }
        for row in rows:
            if row["order_id"] is not None:
                customer_data["orders"].append(
                    {
                        "order_id": row["order_id"],
                        "product": row["product"],
                        "quantity": row["quantity"],
                        "unit_price": row["unit_price"],
                        "order_date": row["order_date"],
                    }
                )

        return customer_data
