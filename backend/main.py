from fastapi import FastAPI  # type: ignore
from db.connection import get_db_conn
from .api.customers import router as customer_router
from .api.orders import router as orders_router

app = FastAPI(title="Junior Developer Assessment API")

app.include_router(customer_router)
app.include_router(orders_router)


@app.get("/health")
def health_check():
    try:
        with get_db_conn() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT name FROM sqlite_master WHERE type='table' AND name='Customers';"
            )

            if not cursor.fetchone():
                return {
                    "status": "unhealthy",
                    "detail": "Database connected but schema missing",
                }

        return {"status": "healthy"}

    except Exception as exc:
        return {"status": "unhealthy", "detail": str(exc)}
