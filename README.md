# Mini Inventory & Order Management API

A simple REST API built using Django and Django REST Framework for managing products, customers and orders.

This project was created as part of a technical internship assignment.

## Technologies Used

- Python
- Django
- Django REST Framework
- Simple JWT
- SQLite
- HTML Browsable API provided by DRF

---

## Features

### Products

- Create product
- List products
- View product details
- Update product
- Delete product
- Search products by name or SKU
- Unique SKU validation

### Customers

- Create customer
- List customers

### Orders

- Create order
- List orders
- View order details
- Update order status
- Cancel order

### Order Items

- Multiple products can be added to one order
- Quantity is stored for each product
- Product price is taken from the database
- Subtotal is calculated by the backend

### Stock Management

When an order is created:

- Available stock is checked
- Stock is decreased automatically
- Order is rejected if there is not enough stock

When an order is cancelled:

- The stock used by the order is added back

### Authentication

JWT authentication is used for API authentication.

---
## Setup
```text
User Login
    ↓
JWT Authentication
    ↓
View Available Products
    ↓
Create / Select Customer
    ↓
Create Order
    ↓
Select Products + Quantity
    ↓
Backend Checks Stock
    ↓
Backend Gets Product Price
    ↓
Calculate Subtotal
    ↓
Calculate Order Total
    ↓
Create Order & Order Items
    ↓
Decrease Product Stock
    ↓
Order Created
```
## Project Flow

The basic flow of the application is:

```text
User Login
    ↓
JWT Authentication
    ↓
View Available Products
    ↓
Create / Select Customer
    ↓
Create Order
    ↓
Select Products + Quantity
    ↓
Backend Checks Stock
    ↓
Backend Gets Product Price
    ↓
Calculate Subtotal
    ↓
Calculate Order Total
    ↓
Create Order & Order Items
    ↓
Decrease Product Stock
    ↓
Order Created

