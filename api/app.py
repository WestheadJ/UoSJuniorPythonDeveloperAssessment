from fastapi import FastAPI, HTTPException
from .db import get_db_conn  # Importing your context manager

app = FastAPI(title="Junior Developer Assessment API")


@app.get("/health")
def health_check():
    """
    Endpoint to verify API and database health.
    """
    try:
        with get_db_conn() as conn:
            # 1. Check if we can run a basic command
            cursor = conn.cursor()

            # 2. Check if our required tables actually exist
            cursor.execute(
                "SELECT name FROM sqlite_master WHERE type='table' AND name='Customers';"
            )
            table_exists = cursor.fetchone()

            if not table_exists:
                return {
                    "status": "unhealthy",
                    "detail": "Database is connected but schema is missing. Run bootstrap script.",
                }

        return {"status": "healthy"}
    except Exception as e:
        return {"status": "unhealthy", "detail": str(e)}
