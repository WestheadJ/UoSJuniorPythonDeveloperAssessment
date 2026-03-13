import csv
import sqlite3
from pathlib import Path
from typing import Iterable, Tuple


# Project paths
ROOT_DIR = Path(__file__).resolve().parent.parent
DB_PATH = ROOT_DIR / "db" / "app.db"
CUSTOMERS_CSV = ROOT_DIR / "data" / "customers.csv"
ORDERS_CSV = ROOT_DIR / "data" / "orders.csv"


# ----------------------------
# Database Connection Utility
# ----------------------------


def get_connection() -> sqlite3.Connection:
    conn = sqlite3.connect(DB_PATH)
    conn.execute("PRAGMA foreign_keys = ON;")
    conn.row_factory = sqlite3.Row
    return conn


# ----------------------------
# Schema Creation
# ----------------------------


def create_customers_table(cursor: sqlite3.Cursor) -> None:
    print("Creating Customers table")

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS Customers (
            customer_id INTEGER PRIMARY KEY,
            first_name TEXT NOT NULL,
            last_name TEXT NOT NULL,
            email TEXT NOT NULL UNIQUE,
            customer_status TEXT NOT NULL
                CHECK (customer_status IN ('active','archived','inactive'))
        )
    """
    )


def create_orders_table(cursor: sqlite3.Cursor) -> None:
    print("Creating Orders table")

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS Orders (
            order_id INTEGER PRIMARY KEY,
            customer_id INTEGER,
            product TEXT NOT NULL,
            quantity INTEGER NOT NULL,
            unit_price REAL NOT NULL,
            order_total REAL GENERATED ALWAYS AS (quantity * unit_price) VIRTUAL,
            order_date TEXT DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (customer_id) REFERENCES Customers(customer_id)
        )
    """
    )


def create_schema(conn: sqlite3.Connection) -> None:
    cursor = conn.cursor()
    create_customers_table(cursor)
    create_orders_table(cursor)
    conn.commit()


def drop_tables(conn: sqlite3.Connection) -> None:
    print("Dropping existing tables")

    cursor = conn.cursor()

    cursor.execute("DROP TABLE IF EXISTS Orders")
    cursor.execute("DROP TABLE IF EXISTS Customers")

    conn.commit()


# ----------------------------
# CSV Parsing
# ----------------------------


def load_customers(csv_path: Path) -> Iterable[Tuple]:
    with open(csv_path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)

        for row in reader:
            yield (
                int(row["customer_id"]),
                row["first_name"],
                row["last_name"],
                row["email"],
                row["customer_status"],
            )


def load_orders(csv_path: Path) -> Iterable[Tuple]:
    with open(csv_path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)

        for row in reader:
            yield (
                int(row["order_id"]),
                int(row["customer_id"]),
                row["product"],
                int(row["quantity"]),
                float(row["unit_price"]),
                row["order_date"],
            )


# ----------------------------
# Data Ingestion
# ----------------------------


def ingest_customers(conn: sqlite3.Connection, csv_path: Path) -> None:
    print("Ingesting customers")

    cursor = conn.cursor()

    cursor.executemany(
        """
        INSERT INTO Customers
        (customer_id, first_name, last_name, email, customer_status)
        VALUES (?, ?, ?, ?, ?)
        """,
        load_customers(csv_path),
    )

    conn.commit()


def ingest_orders(conn: sqlite3.Connection, csv_path: Path) -> None:
    print("Ingesting orders")

    cursor = conn.cursor()

    cursor.executemany(
        """
        INSERT INTO Orders
        (order_id, customer_id, product, quantity, unit_price, order_date)
        VALUES (?, ?, ?, ?, ?, ?)
        """,
        load_orders(csv_path),
    )

    conn.commit()


# ----------------------------
# Bootstrap Orchestration
# ----------------------------


def bootstrap_database() -> None:
    with get_connection() as conn:
        drop_tables(conn)
        create_schema(conn)

        ingest_customers(conn, CUSTOMERS_CSV)
        ingest_orders(conn, ORDERS_CSV)

    print("Database bootstrap complete.")


if __name__ == "__main__":
    bootstrap_database()
