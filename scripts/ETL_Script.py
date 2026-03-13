import pandas as pd
import sqlite3
import os
from pathlib import Path
from datetime import datetime

# --- Configuration & Paths ---
# Ensures the script works regardless of where it's called from
BASE_DIR = Path(__file__).resolve().parent.parent
DB_PATH = BASE_DIR / "db" / "app.db"
OUTPUT_DIR = BASE_DIR / "output"


def run_etl_process():
    """
    Stand-alone ETL job:
    Extracts active customer data, transforms via Pandas, and exports to CSV.
    """
    print("Starting ETL Job...")

    if not OUTPUT_DIR.exists():
        os.makedirs(OUTPUT_DIR)

    try:
        CON = sqlite3.connect(DB_PATH)
        query = """
            SELECT 
                c.customer_id, 
                c.first_name || ' ' || c.last_name AS name,
                c.email, 
                c.customer_status,
                o.order_id, 
                o.product,
                o.quantity, 
                o.unit_price,
                o.order_total
            FROM Customers c
            INNER JOIN Orders o ON c.customer_id = o.customer_id
            WHERE c.customer_status = 'active'
        """
        df = pd.read_sql_query(query, CON)
        CON.close()
    except Exception as e:
        print(f"Database Error: {e}")
        return

    if df.empty:
        print("No data found for active customers with orders. Export cancelled.")
        return

    # Aggregate data to get a per-customer summary
    summary = (
        df.groupby(["customer_id", "name", "email", "customer_status"])
        .agg(
            total_spent=("order_total", "sum"),
            order_count=("order_id", "count"),
            items_purchased=("quantity", "sum"),
        )
        .reset_index()
    )

    try:
        EXPORT_FILE = OUTPUT_DIR / str(
            "customer_summary" + str(datetime.now()) + ".csv"
        )
        summary.to_csv(EXPORT_FILE, index=False)
        print(f"Success! Exported {len(summary)} records to: {EXPORT_FILE}")
    except Exception as e:
        print(f"Export Failed: {e}")

    try:
        EXPORT_FILE = OUTPUT_DIR / str("orders_summary" + str(datetime.now()) + ".csv")
        df.to_csv(EXPORT_FILE, index=False)
        print(f"Success! Exported {len(summary)} records to: {EXPORT_FILE}")
    except Exception as e:
        print(f"Export Failed: {e}")


if __name__ == "__main__":
    run_etl_process()
