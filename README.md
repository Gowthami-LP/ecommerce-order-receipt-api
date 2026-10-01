# E-Commerce Order Receipt API

This project is a beginner-friendly FastAPI application that uses MongoDB and PyMongo to store and combine order data from multiple collections. The goal is to help you understand how a real backend application can gather a profile, product, order, and invoice, then return one clean receipt response.

## 1. Project overview

When a customer buys a product, information is not stored in one table or one collection. The data is spread across:

- profiles
- products
- orders
- invoices

The API exposes a single endpoint:

- GET /api/orders/{order_id}/receipt

This endpoint combines all the related records and returns one receipt JSON response.

## 2. Problem statement

In a real e-commerce system, an order is not complete if you only fetch the order itself. You also need:

- the customer details
- the product details
- the invoice information

This project teaches the basic flow of a receipt aggregation API.

## 3. Why multiple collections are used

MongoDB collections are a natural fit for separate business entities. Instead of storing everything in one giant document, we keep each resource in its own collection:

- profiles stores customer information
- products stores item catalog data
- orders stores order-level details
- invoices stores payment and billing details

This keeps the data organized, easier to manage, and easier to explain in interviews.

## 4. Architecture

The backend follows a simple layered design:

- routes: handle HTTP requests
- services: implement the business logic
- repositories: talk to MongoDB
- models/schemas: define Python objects and request/response structures
- database: create and reuse the MongoDB connection

This keeps the project easy to understand.

## 5. Database design

Database name:

- ecommerce_db

Collections:

- profiles
- products
- orders
- invoices

Data relationships:

- orders.user_id -> profiles._id
- orders.product_id -> products._id
- invoices.order_id -> orders._id

## 6. Collection relationships

```text
profiles
  |
  | _id
  v
orders
  |
  | product_id
  v
products

orders
  |
  | _id
  v
invoices.order_id
```

This means the receipt service reads the order first, then looks up the matching profile and product, and then finds the invoice for that order.

## 7. Project structure

```text
ecommerce-order-receipt-api/
├── app/
│   ├── main.py
│   ├── config/
│   │   ├── __init__.py
│   │   └── settings.py
│   ├── database/
│   │   ├── __init__.py
│   │   └── mongodb.py
│   ├── models/
│   │   ├── __init__.py
│   │   ├── profile.py
│   │   ├── product.py
│   │   ├── order.py
│   │   └── invoice.py
│   ├── repositories/
│   │   ├── __init__.py
│   │   ├── profile_repository.py
│   │   ├── product_repository.py
│   │   ├── order_repository.py
│   │   └── invoice_repository.py
│   ├── routes/
│   │   ├── __init__.py
│   │   ├── profiles.py
│   │   ├── products.py
│   │   ├── orders.py
│   │   ├── invoices.py
│   │   └── receipts.py
│   ├── schemas/
│   │   ├── __init__.py
│   │   ├── profile.py
│   │   ├── product.py
│   │   ├── order.py
│   │   ├── invoice.py
│   │   └── receipt.py
│   └── services/
│       ├── __init__.py
│       └── receipt_service.py
├── tests/
│   ├── __init__.py
│   ├── test_profiles.py
│   ├── test_products.py
│   ├── test_orders.py
│   └── test_receipts.py
├── .env
├── .env.example
├── .gitignore
├── requirements.txt
├── Dockerfile
├── docker-compose.yml
├── README.md
└── app
```

## 8. Installation

### Create and activate a virtual environment

On Windows:

```powershell
cd C:\Users\gowth\DevopsCourse\ecommerce-order-receipt-api
python -m venv venv
.\venv\Scripts\Activate.ps1
```

### Install dependencies

```powershell
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

## 9. .env configuration

Use a local `.env` file for your machine-specific MongoDB settings. This file is intentionally not committed.

```env
MONGO_URI=mongodb://localhost:27017
MONGO_DATABASE=ecommerce_db
```

The tracked template file is:

- `.env.example`

This file is the safe starter copy for new developers and keeps the project configuration consistent without exposing personal/local settings.

This project does not hardcode MongoDB credentials in Python files.

## 10. MongoDB setup

Make sure MongoDB is running locally on port 27017.

You can use a local MongoDB service or a Docker container.

## 11. How to run locally

From the project root:

```powershell
.\venv\Scripts\Activate.ps1
uvicorn app.main:app --reload
```

Open the app here:

- http://127.0.0.1:8000/
- http://127.0.0.1:8000/docs

## 12. Swagger URL

Swagger UI is the easiest way to test the project:

```text
http://127.0.0.1:8000/docs
```

## 13. API list

### Profiles

- POST /api/profiles
- GET /api/profiles/{user_id}
- PUT /api/profiles/{user_id}
- DELETE /api/profiles/{user_id}

### Products

- POST /api/products
- GET /api/products/{product_id}
- PUT /api/products/{product_id}
- DELETE /api/products/{product_id}

### Orders

- POST /api/orders
- GET /api/orders/{order_id}
- PUT /api/orders/{order_id}
- DELETE /api/orders/{order_id}

### Invoices

- POST /api/invoices
- GET /api/invoices/{invoice_id}
- PUT /api/invoices/{invoice_id}
- DELETE /api/invoices/{invoice_id}

### Receipt

- GET /api/orders/{order_id}/receipt

### Health

- GET /
- GET /health

## 14. Sample API requests

### Create a profile

```json
{
  "user_id": "USR1001",
  "name": "Gowthami",
  "email": "gowthami@example.com",
  "phone": "9876543210",
  "address": {
    "city": "Tirupati",
    "state": "Andhra Pradesh",
    "country": "India"
  }
}
```

### Create a product

```json
{
  "product_id": "PROD1001",
  "name": "iPhone 15",
  "category": "Mobile",
  "price": 60000,
  "brand": "Apple",
  "stock": 25
}
```

### Create an order

```json
{
  "order_id": "ORD1001",
  "user_id": "USR1001",
  "product_id": "PROD1001",
  "quantity": 1,
  "status": "delivered",
  "order_date": "2026-09-17"
}
```

### Create an invoice

```json
{
  "invoice_id": "INV1001",
  "order_id": "ORD1001",
  "subtotal": 60000,
  "tax": 10800,
  "discount": 0,
  "shipping": 0,
  "total": 70800,
  "payment_status": "paid"
}
```

## 15. Sample receipt response

```json
{
  "order": {
    "order_id": "ORD1001",
    "quantity": 1,
    "status": "delivered",
    "order_date": "2026-09-17"
  },
  "customer": {
    "user_id": "USR1001",
    "name": "Gowthami",
    "email": "gowthami@example.com",
    "phone": "9876543210",
    "address": {
      "city": "Tirupati",
      "state": "Andhra Pradesh",
      "country": "India"
    }
  },
  "product": {
    "product_id": "PROD1001",
    "name": "iPhone 15",
    "category": "Mobile",
    "brand": "Apple",
    "price": 60000
  },
  "invoice": {
    "invoice_id": "INV1001",
    "subtotal": 60000,
    "tax": 10800,
    "discount": 0,
    "shipping": 0,
    "total": 70800,
    "payment_status": "paid"
  }
}
```

## 16. Error scenarios

The API returns proper HTTP errors:

- 404 when the order is not found
- 404 when the profile is missing
- 404 when the product is missing
- 404 when the invoice is missing

Example:

```json
{
  "detail": "Order not found"
}
```

## 17. Docker setup

Build and run the app with Docker Compose:

```powershell
docker-compose up --build
```

Then open:

- http://localhost:8000/docs

## 18. Docker vs local MongoDB connection

This is important:

- when running locally, the app uses `mongodb://localhost:27017`
- when running inside Docker, the app must use `mongodb://mongodb:27017`

This difference is required because inside the Docker container, `localhost` points to the container itself, not your MongoDB container.

The `docker-compose.yml` file sets the environment variable for the app container:

```yaml
MONGO_URI: mongodb://mongodb:27017
```

## 19. Testing

Run the tests with:

```powershell
python -m pytest -q
```

The tests check:

- profile creation and retrieval
- product creation and retrieval
- order creation and retrieval
- receipt response
- missing order handling
- missing product handling
- missing invoice handling

## 20. MongoDB $lookup explanation

The first implementation in this project does not use `$lookup` because the goal is to understand the business logic at the application layer. We first do separate PyMongo reads in the service layer:

1. fetch the order
2. fetch the profile using `user_id`
3. fetch the product using `product_id`
4. fetch the invoice using `order_id`
5. combine them into one response

Later, you can improve this with MongoDB aggregation using `$lookup` to join collections in the database layer. That is a second step and a different design.

## 21. Future improvements

Possible next steps:

- add pagination
- add search filters
- add stock validation
- add soft-delete support
- add more advanced tests
- add database indexing
- add MongoDB aggregation with `$lookup`

## 22. Interview explanation

A good interview answer for this project is:

> This API is a receipt aggregation service. It stores customer, product, order, and invoice details in separate MongoDB collections. The route receives an order ID, the service fetches the order, then reads the related profile and product, and finally looks up the matching invoice. After that, it combines everything into one JSON response. This is a simple example of data aggregation across multiple collections.

## 23. Request flow example

A request like this:

```text
GET /api/orders/ORD1001/receipt
```

follows this flow:

1. Swagger sends the request
2. FastAPI route receives the request
3. route calls the service
4. service fetches order from orders collection
5. service fetches profile from profiles collection
6. service fetches product from products collection
7. service fetches invoice from invoices collection
8. service combines the data into one receipt object
9. Pydantic serializes it
10. Swagger displays the response

## 25. Beginner notes

This project intentionally avoids complex enterprise patterns. It focuses on the fundamental skills you need to understand:

- FastAPI routing
- Pydantic validation
- MongoDB collections
- repository layer
- service layer
- API response modeling
- basic Docker setup

This is clean, practical, and interview-friendly.
