import sqlite3
from pathlib import Path
from contextlib import contextmanager

DB_PATH = Path(__file__).parent.parent / "db" / "app.db"


@contextmanager
def get_db_conn():
    """
    A generator that 'yields' a connection.
    When the 'with' block finishes, it 'closes' the connection.
    """
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    try:
        yield conn
    finally:
        conn.close()
