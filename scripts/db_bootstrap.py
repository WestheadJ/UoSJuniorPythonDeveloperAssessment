import csv
import sqlite3
from pathlib import Path

# Get the root directory of the project
ROOT_DIR = Path(__file__).parent.parent

# Define paths for the database, and the datasets
DB_PATH = ROOT_DIR / "db" / "app.db"
CUSTOMERS_CSV = ROOT_DIR / "data" / "customers.csv"
ORDERS_CSV = ROOT_DIR / "data" / "orders.csv"

CON = sqlite3.connect(DB_PATH)
CON.execute("PRAGMA foreign_keys = ON;")
CUR = CON.cursor()


def create_customers_table(CUR, CON):
    print("Creating customers")
    CUR.execute(
        """CREATE TABLE IF NOT EXISTS Customers (customer_id INTEGER PRIMARY KEY,
        first_name TEXT NOT NULL, 
        last_name TEXT NOT NULL,
        email TEXT NOT NULL UNIQUE,
        status TEXT NOT NULL CHECK (status IN ('active', 'archived', 'inactive')));
"""
    )
    CON.commit()


def create_orders_table(CUR, CON):
    print("Creating orders")
    CUR.execute(
        """CREATE TABLE IF NOT EXISTS Orders (
    order_id INTEGER PRIMARY KEY,
    customer_id INTEGER NOT NULL,
    product TEXT NOT NULL,
    quantity INTEGER NOT NULL CHECK (quantity > 0),
    unit_price REAL NOT NULL CHECK (unit_price >= 0),
    status TEXT NOT NULL CHECK (status IN ('Pending', 'Shipped', 'Delivered', 'Cancelled')),
    order_date TEXT NOT NULL, -- Format: YYYY-MM-DD
    FOREIGN KEY (customer_id) REFERENCES Customers(customer_id)
);
"""
    )
    CON.commit()


def create_tables(CUR, CON):
    create_customers_table(CUR, CON)
    create_orders_table(CUR, CON)


def drop_tables(CUR, CON):
    print("Dropping Tables...")
    CUR.execute("DROP TABLE IF EXISTS Orders")
    CUR.execute("DROP TABLE IF EXISTS Customers")
    CON.commit()


def bootstrap_customers(CUR, CON, csv_path):
    print("Ingesting Customers...")
    with open(csv_path, mode="r") as f:
        reader = csv.DictReader(f)
        batch_data = [
            (
                int(row["customer_id"]),
                row["first_name"],
                row["last_name"],
                row["email"],
                row["status"],
            )
            for row in reader
        ]

    CUR.executemany(
        "INSERT INTO Customers (customer_id, first_name, last_name, email, status) VALUES (?, ?, ?, ?, ?)",
        batch_data,
    )
    CON.commit()


def bootstrap_orders(CUR, CON, csv_path):
    print("Ingesting orders...")
    with open(csv_path, mode="r") as f:
        reader = csv.DictReader(f)
        batch_data = [
            (
                int(row["order_id"]),
                int(row["customer_id"]),
                row["product"],
                int(row["quantity"]),
                float(row["unit_price"]),
                row["status"],
                row["order_date"],
            )
            for row in reader
        ]

    # Use CON (matching your global variable)
    CUR.executemany(
        "INSERT INTO Orders (order_id,customer_id,product , quantity, unit_price, status,order_date) VALUES (?, ?, ?, ?, ?,?,?)",
        batch_data,
    )
    CON.commit()


if __name__ == "__main__":
    drop_tables(CUR, CON)
    create_tables(CUR, CON)
    bootstrap_customers(CUR, CON, CUSTOMERS_CSV)
    bootstrap_orders(CUR, CON, ORDERS_CSV)
    CON.close()
