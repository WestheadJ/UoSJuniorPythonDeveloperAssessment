import sqlite3
from pathlib import Path

# Get the root directory of the project
ROOT_DIR = Path(__file__).parent.parent

# Define paths for the database, and the datasets
DB_PATH = ROOT_DIR / "db" / "app.db"
CON = sqlite3.connect(DB_PATH)
CUR = CON.cursor()

if __name__ == "__main__":
    CUR.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = CUR.fetchall()
    print(f"Tables found: {[t[0] for t in tables]}")

    for table_name in [t[0] for t in tables]:
        print(f"\nSchema for table: {table_name}")
        # 2. Get column details: (id, name, type, notnull, default_value, pk)
        CUR.execute(f"PRAGMA table_info({table_name});")
        columns = CUR.fetchall()
        for col in columns:
            print(f"  - {col[1]} ({col[2]}) {'[PK]' if col[5] else ''}")

        # 3. Check row counts to ensure ingestion worked
        CUR.execute(f"SELECT COUNT(*) FROM {table_name};")
        count = CUR.fetchone()[0]
        print(f"Total rows: {count}")

        CUR.execute(f"SELECT * FROM {table_name}")
        items = CUR.fetchmany(5)
        for i in items:
            print(i)
