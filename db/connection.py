import sqlite3
from pathlib import Path
from contextlib import contextmanager

BASE_DIR = Path(__file__).resolve().parent.parent
DB_PATH = BASE_DIR / "db" / "app.db"


@contextmanager
def get_db_conn():
    """
    Context manager for SQLite database connection.
    Ensures foreign keys are on and connection is safely closed.
    Usage:
        with get_db_conn() as conn:
            ...
    """
    conn = sqlite3.connect(DB_PATH)
    conn.execute("PRAGMA foreign_keys = ON;")
    conn.row_factory = sqlite3.Row  # Enables dict-like access for rows

    try:
        yield conn
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()
