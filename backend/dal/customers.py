# dal/customers.py

from db.connection import get_db_conn

CUSTOMER_ORDERS_QUERY = """
SELECT 
    c.customer_id,
    c.first_name,
    c.last_name,
    c.email,
    c.customer_status,
    o.order_id,
    o.product,
    o.quantity,
    o.unit_price,
    o.order_date
FROM Customers c
LEFT JOIN Orders o ON c.customer_id = o.customer_id
WHERE c.customer_id = ?
"""


def get_customer_orders(customer_id: int):
    with get_db_conn() as conn:
        cursor = conn.cursor()
        cursor.execute(CUSTOMER_ORDERS_QUERY, (customer_id,))
        return cursor.fetchall()
