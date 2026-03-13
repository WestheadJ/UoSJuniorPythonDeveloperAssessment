import sqlite3
from pathlib import Path
from datetime import datetime
import pandas as pd


# ----------------------------
# Paths / Configuration
# ----------------------------

BASE_DIR = Path(__file__).resolve().parent.parent
DB_PATH = BASE_DIR / "db" / "app.db"
OUTPUT_DIR = BASE_DIR / "output"


QUERY_ACTIVE_CUSTOMER_ORDERS = """
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
INNER JOIN Orders o
    ON c.customer_id = o.customer_id
WHERE c.customer_status = 'active'
"""


# ----------------------------
# Extract
# ----------------------------


def extract_orders() -> pd.DataFrame:
    """Extract active customer order data from SQLite."""

    try:
        with sqlite3.connect(DB_PATH) as conn:
            df = pd.read_sql_query(QUERY_ACTIVE_CUSTOMER_ORDERS, conn)
        return df

    except sqlite3.Error as err:
        print(f"Database error: {err}")
        return pd.DataFrame()


# ----------------------------
# Transform
# ----------------------------


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


# ----------------------------
# Load (Export)
# ----------------------------


def export_csv(df: pd.DataFrame, prefix: str) -> None:
    """Export dataframe to timestamped CSV."""

    OUTPUT_DIR.mkdir(exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    file_path = OUTPUT_DIR / f"{prefix}_{timestamp}.csv"

    try:
        df.to_csv(file_path, index=False)
        print(f"Exported {len(df)} records → {file_path}")

    except Exception as err:
        print(f"Export failed: {err}")


# ----------------------------
# ETL Orchestration
# ----------------------------


def run_etl_process() -> None:
    """Run the full ETL pipeline."""

    print("Starting ETL job...")

    # Extract
    orders_df = extract_orders()

    if orders_df.empty:
        print("No active customer order data found. ETL cancelled.")
        return

    # Transform
    summary_df = transform_customer_summary(orders_df)

    # Load
    export_csv(summary_df, "customer_summary")
    export_csv(orders_df, "orders_summary")

    print("ETL job completed.")


if __name__ == "__main__":
    run_etl_process()
