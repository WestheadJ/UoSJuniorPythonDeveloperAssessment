
# API Design Specification

*This document defines the interface and communication standards for the Project API.*

## Overview

The API is built using **FastAPI** to provide a high-performance, validated interface for retrieving customer and order data. It interfaces directly with the SQLite database populated during the Task 1 bootstrap process.

## Endpoints

### 1. Health Check

Evaluates the operational status of the API and its connection to the data layer.

* **Endpoint:** `/health`
* **Method:** `GET`
* **Success Response:**
* **Code:** `200 OK`
* **Content:** `{"status": "healthy"}`
* **Scenario:** The FastAPI server is running and the SQLite database is accessible and responsive to queries.


* **Error Response:**
* **Code:** `500 Internal Server Error`
* **Content:** `{"status": "unhealthy", "detail": "Database connection failed"}`
* **Scenario:** The server is running, but the database file (`app.db`) is missing, locked, or corrupted.



### 2. Get Customer Orders

Retrieves a specific customer's profile and their associated order history.

* **Endpoint:** `/customers/{customer_id}/orders`
* **Method:** `GET`
* **URL Params:** `customer_id=[integer]`
* 
**Description:** Performs a relational lookup to return a single customer record and a nested list of all orders belonging to that ID.


* **Success Response:**
* **Code:** `200 OK`
* **Content:** 
```json
{
"customer": {
"customer_id": 1,
"first_name": "James",
"last_name": "Smith",
"email": "james.smith@email.com",
"status": "active"
},
"orders": [
{
"order_id": 101,
"product": "Wireless Mouse",
"quantity": 1,
"unit_price": 25.0,
"total_price": 25.0,
"status": "Shipped",
"order_date": "2026-03-10"
}
]
}
```
## Error Handling

| Scenario | Status Code | JSON Payload |
| :--- | :--- | :--- |
| **Customer Not Found** | 
`404 Not Found` | ```{"detail": "Customer with ID {id} not found"}` |
| **Invalid ID Format** | `422 Unprocessable Entity` | `{"detail": "ID must be an integer"}` |

## Implementation Details

### Data Validation
The API utilizes **Python Type Hints** and **Pydantic** (via FastAPI) to automatically validate that `customer_id` is an integer before any database logic is executed. This ensures "Clean Code" principles and prevents common injection errors by rejecting non-numeric input at the gateway.

### Error Handling Logic
The application uses FastAPI’s `HTTPException` class to manage edge cases:
* **Existence Check:** A query is performed to verify the customer exists in the database. If the ID is missing, a `404 Not Found` is raised.
* **Empty Result Sets:** If a customer exists but has no orders, the API returns a `200 OK` with an empty orders list (`"orders": []`). This confirms the customer was found but has no history, maintaining REST compliance.

### Database Session Management
To ensure the script is repeatable and efficient, the API uses a context manager to open and close database connections for each request. This prevents memory leaks and ensures the database does not remain locked during concurrent operations.
