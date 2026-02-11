# 🛒 Mini E-Commerce API

> A RESTful Mini E-Commerce API built with FastAPI, featuring JWT authentication, role-based authorization (Admin & Customer), product inventory management, cart operations, and order processing with transactional data integrity.

---

## 📋 Table of Contents

- [Features](#-features)
- [Tech Stack](#-tech-stack)
- [Project Structure](#-project-structure)
- [Getting Started](#-getting-started)
  - [Prerequisites](#prerequisites)
  - [Installation](#installation)
  - [Environment Variables](#environment-variables)
  - [Running the Application](#running-the-application)
- [API Documentation](#-api-documentation)
- [API Endpoints](#-api-endpoints)
- [Authentication & Authorization](#-authentication--authorization)
- [Database Schema](#️-database-schema)
- [Key Architectural Decisions](#️-key-architectural-decisions)
- [Assumptions & Constraints](#-assumptions--constraints)
- [Author](#-author)

---

## ✨ Features

### Core Functionality
- 🔐 **JWT Authentication** - Secure token-based authentication system
- 👥 **Role-Based Access Control (RBAC)** - Admin and Customer roles with different permissions
- 📦 **Product Management** - Complete CRUD operations for products
- 🛒 **Shopping Cart** - Add, update, remove items from cart
- 📋 **Order Processing** - Create and manage orders with transaction integrity
- 💾 **Inventory Management** - Real-time stock tracking and updates
- 📸 **Image Upload** - Product image storage and retrieval
- 🔍 **Search & Filter** - Advanced product search capabilities

### Security Features
- Password hashing with bcrypt
- JWT token-based authentication
- Role-based authorization middleware
- SQL injection protection via SQLAlchemy ORM
- CORS configuration

### Technical Features
- RESTful API design principles
- Comprehensive API documentation with Swagger/OpenAPI
- Database transactions for data integrity
- Request validation with Pydantic schemas
- Proper error handling and status codes

---

## 🛠 Tech Stack

- **Framework**: [FastAPI](https://fastapi.tiangolo.com/) - Modern, fast web framework for building APIs
- **Database**: SQLAlchemy ORM with SQLite/PostgreSQL
- **Authentication**: JWT (JSON Web Tokens)
- **Validation**: Pydantic models
- **Password Hashing**: Passlib with bcrypt
- **Documentation**: Automatic OpenAPI (Swagger) documentation
- **Python Version**: 3.9+

---

## 📁 Project Structure

```
mini_e-Commerce_api/
├── core/                  # Core application configuration
│   ├── __init__.py
│   ├── config.py          # Application settings and configuration
│   ├── database.py        # Database connection and session management
|   └── dependencies.py  # Dependency injection auth
│   
│
├── models/                # Database models (SQLAlchemy)
│   ├── __init__.py
│   ├── user.py           # User model
│   ├── product.py        # Product model
│   ├── cart.py           # Shopping cart model
│   └── order.py          # Order model
│
├── schemas/              # Pydantic schemas for request/response validation
│   ├── __init__.py
│   ├── user.py          # User schemas
│   ├── product.py       # Product schemas
│   ├── cart.py          # Cart schemas
│   └── order.py         # Order schemas
│
├── routers/              # API route handlers
│   ├── __init__.py
│   ├── auth.py          # Authentication endpoints
│   ├── users.py         # User management endpoints
│   ├── products.py      # Product endpoints
│   ├── cart.py          # Shopping cart endpoints
│   └── orders.py        # Order management endpoints
│
├── utils/                # Utility functions
│   └── security.py        # Security utilities (JWT, password hashing)
│
├── static/               # Static files
│   └── products/        # Product images storage
│
├── main.py              # Application entry point
├── requirements.txt     # Python dependencies
├── .env                # Environment variables template
└── README.md           # This file
```

---

## 🚀 Getting Started

### Prerequisites

Before you begin, ensure you have the following installed:
- Python 3.9 or higher
- pip (Python package manager)
- Virtual environment tool (venv or virtualenv)

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/mirzasalem/mini_e-Commerce_api.git
   cd mini_e-Commerce_api
   ```

2. **Create and activate a virtual environment**

   On Windows:
   ```bash
   python -m venv venv
   venv\Scripts\activate
   ```

   On Linux:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

### Environment Variables

Create a `.env` file in the root directory:

```env
# Database Configuration
DATABASE_URL=postgresql://postgres:ur_password@localhost:5432/mini_ecommerce

# Security
SECRET_KEY=my-super-secret-key-minimum-32-characters-long-please

# Optional (will use defaults from config.py if not specified)
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
DEBUG=True
```

### Running the Application

1. **Start the development server**
   ```bash
   uvicorn main:app --reload
   ```

2. **Access the application**
   - API Base URL: `http://localhost:8000`
   - Interactive API Docs (Swagger): `http://localhost:8000/docs`
   - Alternative API Docs (ReDoc): `http://localhost:8000/redoc`

---

## 📚 API Documentation

Once the application is running, access the interactive API documentation at:

- **Swagger UI**: [http://localhost:8000/docs](http://localhost:8000/docs)
- **ReDoc**: [http://localhost:8000/redoc](http://localhost:8000/redoc)

These provide:
- Complete API endpoint documentation
- Request/response schemas
- Try-it-out functionality
- Authentication testing

---

## 🔌 API Endpoints

### Authentication

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| POST | `/api/auth/register` | Register new user | ❌ |
| POST | `/api/auth/login` | User login | ❌ |
| POST | `/api/auth/logout` | User logout | ✅ |
| POST | `/api/auth/refresh` | Refresh access token | ✅ |

### Users

| Method | Endpoint | Description | Auth Required | Role |
|--------|----------|-------------|---------------|------|
| GET | `/api/users/me` | Get current user profile | ✅ | Any |
| PUT | `/api/users/me` | Update current user | ✅ | Any |
| GET | `/api/users` | Get all users | ✅ | Admin |
| GET | `/api/users/{user_id}` | Get user by ID | ✅ | Admin |
| DELETE | `/api/users/{user_id}` | Delete user | ✅ | Admin |

### Products

| Method | Endpoint | Description | Auth Required | Role |
|--------|----------|-------------|---------------|------|
| GET | `/api/products` | Get all products | ❌ | - |
| GET | `/api/products/{product_id}` | Get product by ID | ❌ | - |
| POST | `/api/products` | Create new product | ✅ | Admin |
| PUT | `/api/products/{product_id}` | Update product | ✅ | Admin |
| DELETE | `/api/products/{product_id}` | Delete product | ✅ | Admin |
| POST | `/api/products/{product_id}/image` | Upload product image | ✅ | Admin |
| GET | `/api/products/search` | Search products | ❌ | - |

### Shopping Cart

| Method | Endpoint | Description | Auth Required | Role |
|--------|----------|-------------|---------------|------|
| GET | `/api/cart` | Get user's cart | ✅ | Customer |
| POST | `/api/cart/items` | Add item to cart | ✅ | Customer |
| PUT | `/api/cart/items/{item_id}` | Update cart item quantity | ✅ | Customer |
| DELETE | `/api/cart/items/{item_id}` | Remove item from cart | ✅ | Customer |
| DELETE | `/api/cart` | Clear entire cart | ✅ | Customer |

### Orders

| Method | Endpoint | Description | Auth Required | Role |
|--------|----------|-------------|---------------|------|
| GET | `/api/orders` | Get all orders | ✅ | Admin |
| GET | `/api/orders/my-orders` | Get current user's orders | ✅ | Customer |
| GET | `/api/orders/{order_id}` | Get order by ID | ✅ | Any |
| POST | `/api/orders` | Create new order | ✅ | Customer |
| PUT | `/api/orders/{order_id}/status` | Update order status | ✅ | Admin |
| DELETE | `/api/orders/{order_id}` | Cancel order | ✅ | Customer/Admin |

---

## 🔐 Authentication & Authorization

### Registration Flow

```json
POST /api/auth/register
{
  "email": "user@example.com",
  "password": "SecurePassword123!",
  "full_name": "user_salem",
  "role": "customer"  // or "admin"
}
```

**Response:**
```json
{
  "id": 2,
  "email": "usdsder@example.com",
  "username": "stdsdsring",
  "role": "customer",
  "created_at": "2026-02-11T22:29:23.198283",
  "order_cancellation_count": 0
}
```

### Login Flow

```json
POST /api/auth/login
{
  "email": "user@example.com",
  "password": "SecurePassword123!"
}
```

**Response:**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJ1c2VyQGV4YW1wbGUuY29tIiwicm9sZSI6ImFkbWluIiwiZXhwIjoxNzcwODUwODU2fQ.vugm9ZsPody3dXs693lh8yDim3tVZBp7JKi8pNAIkqc",
  "token_type": "bearer",
  "user": {
    "id": 1,
    "email": "user@example.com",
    "username": "admin",
    "role": "admin",
    "created_at": "2026-02-11T20:47:25.928763",
    "order_cancellation_count": 0
  }
}
```

### Using the Token

Include the JWT token in the Authorization header for protected endpoints:

```
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

### Role-Based Access

- **Customer Role**: Can manage their cart, place orders, and view their order history
- **Admin Role**: Full access to all endpoints, can manage products, users, and all orders

---
# 🗄️ Database Schema

This project uses a relational database design to manage users, products, carts, and orders.

---

## 👤 User

Stores registered user information.

| Column | Type | Constraints |
|--------|------|------------|
| id | Integer | Primary Key |
| email | String | Unique, Not Null |
| hashed_password | String | Not Null |
| full_name | String | Not Null |
| role | Enum | Default: CUSTOMER |
| created_at | DateTime |  |
| updated_at | DateTime |  |

**Relationships**
- One User has **one Cart**
- One User can have **many Orders**

---

## 📦 Product

Stores product details.

| Column | Type | Constraints |
|--------|------|------------|
| id | Integer | Primary Key |
| name | String | Not Null |
| description | Text |  |
| price | Decimal | Not Null |
| stock_quantity | Integer | Not Null |
| category | String |  |
| image_url | String |  |
| created_at | DateTime |  |
| updated_at | DateTime |  |

**Relationships**
- One Product can exist in **many CartItems**
- One Product can exist in **many OrderItems**

---

## 🛒 Cart

Represents a user's shopping cart.

| Column | Type | Constraints |
|--------|------|------------|
| id | Integer | Primary Key |
| user_id | Integer | Foreign Key → User(id) |
| created_at | DateTime |  |
| updated_at | DateTime |  |

**Relationships**
- One Cart belongs to **one User**
- One Cart contains **many CartItems**

---

## 🧾 CartItem

Represents products inside a cart.

| Column | Type | Constraints |
|--------|------|------------|
| id | Integer | Primary Key |
| cart_id | Integer | Foreign Key → Cart(id) |
| product_id | Integer | Foreign Key → Product(id) |
| quantity | Integer | Not Null |
| price_at_time | Decimal | Not Null |

---

## 📦 Order

Represents a completed purchase.

| Column | Type | Constraints |
|--------|------|------------|
| id | Integer | Primary Key |
| user_id | Integer | Foreign Key → User(id) |
| total_amount | Decimal | Not Null |
| status | Enum | Default: PENDING |
| descriptions | Text |  |
| created_at | DateTime |  |
| updated_at | DateTime |  |

**Relationships**
- One Order belongs to **one User**
- One Order contains **many OrderItems**

---

## 🧾 OrderItem

Represents individual products within an order.

| Column | Type | Constraints |
|--------|------|------------|
| id | Integer | Primary Key |
| order_id | Integer | Foreign Key → Order(id) |
| product_id | Integer | Foreign Key → Product(id) |
| quantity | Integer | Not Null |
| price_at_time | Decimal | Not Null |

---

## 🏗️ Key Architectural Decisions

### 1. Framework: FastAPI
**Why FastAPI?**
- Modern async/await support for high performance
- Automatic API documentation (Swagger/OpenAPI)
- Built-in request validation with Pydantic
- Type hints and IDE support
- Fast development and excellent developer experience

### 2. Database: SQLAlchemy ORM
**Why SQLAlchemy?**
- Database agnostic (easy migration from SQLite to PostgreSQL)
- Mature and well-tested ORM with 15+ years of development
- Built-in transaction management for data integrity
- Alembic integration for database migrations
- Supports both high-level ORM and low-level SQL operations

### 3. Authentication: JWT (JSON Web Tokens)
**Why JWT?**
- Stateless authentication (no server-side session storage)
- Scalable across multiple servers/instances
- Industry standard for REST APIs
- Easy integration with mobile and web applications
- Includes user role information in token payload

**Security Implementation:**
- Algorithm: HS256 (HMAC with SHA-256)
- Token expiry: 30 minutes (configurable)
- Password hashing: Bcrypt with automatic salt
- Protected routes via dependency injection

### 4. Project Structure: Modular Architecture

**Benefits:**
- Clear separation of concerns
- Easy to test individual components
- Scalable and maintainable codebase
- Facilitates team collaboration
- Can be easily refactored into microservices

### 5. Transaction Management
**Critical Transaction Points:**
1. **Order Placement**: Stock validation → Order creation → Inventory deduction → Cart clearing (all-or-nothing)
2. **Stock Updates**: Validation → Update → Logging (atomic operation)
3. **Cart to Order**: Lock products → Validate → Create order → Update inventory (with rollback on failure)

**Implementation:**
- Database-level transactions via SQLAlchemy
- Automatic rollback on exceptions
- Ensures data consistency across concurrent operations

---

## 📋 Assumptions & Constraints

### Business Assumptions

**Product & Pricing:**
- Single currency (BD) for all transactions
- Single image per product
- Simple flat category structure (no hierarchical categories)

**Order Processing:**
- No real-time shipping cost calculation
- Order status managed manually by admin
- Orders cannot be modified after placement
- Cancellation allowed only before shipping

**Customer Experience:**
- Anonymous browsing allowed (authentication required for purchase)
- No guest checkout (account required)
- One cart per user

### Technical Assumptions

**Authentication & Security:**
- JWT token-based authentication (stateless)
- Two roles: Admin and Customer (no granular permissions)
- HTTPS handled by reverse proxy (Nginx/Apache)
- No two-factor authentication (2FA)
- Password reset via email (future feature)

**Database:**
- SQLite for development (zero configuration)
- PostgreSQL for production (recommended)
- Single database instance (no replication)
- Connection pooling via SQLAlchemy

**File Storage:**
- Local filesystem for product images
- No CDN integration
- 5MB file size limit
- Allowed formats: JPEG, PNG, WebP

**Performance:**
- No caching layer (Redis can be added)
- No background job queue (Celery can be added)
- Basic database search (no Elasticsearch)
- Suitable for small to medium traffic

### Data Integrity Measures

**Stock Management:**
- Stock validation at multiple checkpoints (cart add, quantity update, checkout)
- Atomic stock deduction during order placement
- Database constraints prevent negative inventory
- Immediate stock return on order cancellation

**Order Processing:**
- Order total calculated server-side (never trust client)
- Price snapshot preserved in OrderItems
- Transaction isolation prevents race conditions

---

<!-- pip install pydantic[email] -->

## 👨 Author

Mirza Salem  
[GitHub](https://github.com/mirzasalem/) | [LinkedIn](https://www.linkedin.com/in/mirzasalem/) | [Portfolio](https://mirzasalem.vercel.app/)

## 💼 About This Project

Created as a portfolio E-Commerce project to demonstrate backend development skills for job applications.
