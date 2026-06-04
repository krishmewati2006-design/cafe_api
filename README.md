# Cafe API

A robust backend API built with FastAPI for managing cafe operations, including staff management, menu control, order processing, and financial reporting.

## Features

- Staff Management: Secure registration and authentication using JWT (JSON Web Tokens).
- Menu Management: Full CRUD (Create, Read, Update, Delete) operations for menu items with role-based access control.
- Order Processing: Create orders, add items to active orders, and track order status.
- Financial Reporting: Generate daily, monthly, and yearly revenue reports (Manager exclusive).
- Role-Based Access Control (RBAC): Distinct permissions for Staff and Managers.
- Database Migrations: Managed with Alembic for easy schema updates.

## Tech Stack

- Framework: FastAPI
- ORM: SQLAlchemy 2.0
- Database Migrations: Alembic
- Security: Jose (JWT), Passlib (Bcrypt)
- Validation: Pydantic v2
- Web Server: Uvicorn

## Project Structure

```text
cafe_api/
├── alembic/              # Database migration scripts
├── routers/              # API route handlers
│   ├── menu.py           # Menu CRUD endpoints
│   ├── orders.py         # Order management endpoints
│   ├── reports.py        # Revenue reporting endpoints
│   └── staff.py          # Auth and staff endpoints
├── auth.py               # Security and JWT logic
├── database.py           # Database connection and session setup
├── main.py               # Application entry point
├── models.py             # SQLAlchemy database models
├── schemas.py            # Pydantic models for request/response
├── requirements.txt      # Project dependencies
└── alembic.ini           # Alembic configuration
```

## Setup and Installation

### 1. Clone the Repository
```bash
git clone <repository-url>
cd cafe_api
```

### 2. Create a Virtual Environment
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables
Create a `.env` file in the root directory:
```env
DATABASE_URL=postgresql://user:password@localhost/dbname
SECRET_KEY=your_super_secret_key_here
```

### 5. Run Database Migrations
```bash
alembic upgrade head
```

## API Endpoints

### Staff & Auth
- POST /register: Create a new staff account.
- POST /login: Authenticate and receive a JWT token.

### Menu (Manager Required for Write)
- GET /menu: Retrieve all menu items.
- POST /menu: Add a new item to the menu.
- PUT /menu/{item_id}: Update an existing menu item.
- DELETE /menu/{item_id}: Remove an item from the menu.

### Orders
- POST /orders: Start a new order.
- POST /orders/{order_id}/items: Add items to an existing order.
- GET /orders/{order_id}: Retrieve order details.
- PATCH /orders/{order_id}/close: Mark an order as closed.
- GET /orders/: List all orders (Manager Only).

### Reports (Manager Only)
- GET /reports/daily: Get today's total revenue.
- GET /reports/monthly: Get revenue for the current month.
- GET /reports/yearly: Get revenue for the current year.

## Running the App

Start the development server with:
```bash
fastapi dev main.py
```
The API will be available at http://127.0.0.1:8000.
Access the interactive documentation (Swagger UI) at http://127.0.0.1:8000/docs.

## Authentication
This API uses Bearer Token authentication. To access protected routes:
1. Login via /login to get an access_token.
2. Include the token in the Authorization header of your requests:
   Authorization: Bearer <your_token>

---
*Created for cafe management efficiency.*
