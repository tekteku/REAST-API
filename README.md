# Library REST API

A production-ready REST API for managing library books, members, and loans built with FastAPI and PostgreSQL.

## Features

- **Book Management**: Create, read, update, delete books
- **Member Management**: Register members, manage profiles
- **Loan System**: Borrow and return books with business logic validation
- **Search**: Search books by title, author, or ISBN
- **Pagination**: All list endpoints support pagination
- **REST API**: Full REST API with proper HTTP status codes
- **API Documentation**: Interactive Swagger documentation

## Project Structure

```
library-api/
├── app/
│   ├── __init__.py
│   ├── main.py                 # FastAPI app entry point
│   ├── database.py             # SQLAlchemy setup
│   ├── models.py               # ORM models
│   ├── schemas/                # Pydantic schemas
│   │   ├── __init__.py
│   │   ├── book.py
│   │   ├── member.py
│   │   └── loan.py
│   ├── routers/                # API endpoints
│   │   ├── __init__.py
│   │   ├── books.py
│   │   ├── members.py
│   │   └── loans.py
│   ├── repositories/           # Data access layer
│   │   ├── __init__.py
│   │   ├── book_repository.py
│   │   ├── member_repository.py
│   │   └── loan_repository.py
│   └── services/               # Business logic layer
│       ├── __init__.py
│       └── loan_service.py
├── requirements.txt            # Python dependencies
├── .env.example               # Environment variables template
└── README.md                  # This file
```

## Architecture

This project follows **Layered Architecture** pattern:

### Layer Responsibilities

| Layer | Responsibility |
|-------|-----------------|
| **Router** | Receives HTTP requests, validates with Pydantic, calls service |
| **Service** | Contains business rules (max 3 loans, book availability, member validation) |
| **Repository** | Executes SQL queries against PostgreSQL, returns data objects |
| **Database** | Stores actual data in PostgreSQL |

#### Flow Example: Borrow a Book

```
HTTP Request
    ↓
Router (books.py) - validates input
    ↓
LoanService - enforces business rules
    ↓
LoanRepository - executes SQL queries
    ↓
PostgreSQL Database
```

## Setup Instructions

### Prerequisites

- Python 3.9+
- PostgreSQL 12+
- pip

### 1. Clone the repository

```bash
git clone <repository-url>
cd library-api
```

### 2. Create virtual environment

```bash
python -m venv venv
```

On Windows:
```bash
venv\Scripts\activate
```

On macOS/Linux:
```bash
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Setup environment variables

```bash
cp .env.example .env
```

Edit `.env` and update PostgreSQL connection string:
```
DATABASE_URL=postgresql://username:password@localhost:5432/library_db
```

### 5. Create database

```sql
CREATE DATABASE library_db;
```

### 6. Run the application

```bash
python -m uvicorn app.main:app --reload
```

The API will be available at `http://localhost:8000`

- API Documentation: `http://localhost:8000/api/docs`
- ReDoc: `http://localhost:8000/api/redoc`

## API Endpoints

### Books
- `POST /books` - Create a new book
- `GET /books` - List all books
- `GET /books/search?q=<query>` - Search books
- `GET /books/{book_id}` - Get book details
- `PUT /books/{book_id}` - Update a book
- `DELETE /books/{book_id}` - Delete a book

### Members
- `POST /members` - Register new member
- `GET /members` - List all members
- `GET /members/search?q=<query>` - Search members
- `GET /members/{member_id}` - Get member details
- `PUT /members/{member_id}` - Update member
- `DELETE /members/{member_id}` - Deactivate member

### Loans
- `POST /loans/borrow` - Borrow a book
- `POST /loans/{loan_id}/return` - Return a book
- `GET /loans` - List all loans
- `GET /loans/member/{member_id}` - Get member's active loans
- `GET /loans/member/{member_id}/history` - Get member's loan history
- `GET /loans/overdue` - Get overdue loans

## Business Rules

### Borrowing a Book

1. Member must exist and be active
2. Book must exist and have available copies
3. Member cannot have more than **3 active loans**
4. Member cannot borrow the same book twice while it's unreturned

### Returning a Book

1. Loan must exist and be active
2. Book availability is restored upon return
3. Fine calculation (optional): $1 per day overdue

## Example Usage

### Create a Book
```bash
curl -X POST "http://localhost:8000/books" \
  -H "Content-Type: application/json" \
  -d '{
    "isbn": "978-0-596-00712-6",
    "title": "Learning Python",
    "author": "Mark Lutz",
    "description": "A comprehensive guide to Python programming",
    "total_copies": 3
  }'
```

### Register a Member
```bash
curl -X POST "http://localhost:8000/members" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Taher",
    "email": "taherch2025@gmail.com",
    "phone": "+1-555-0123",
    "address": "123 Main St, Anytown, USA"
  }'
```

### Borrow a Book
```bash
curl -X POST "http://localhost:8000/loans/borrow" \
  -H "Content-Type: application/json" \
  -d '{
    "book_id": 1,
    "member_id": 1,
    "loan_duration_days": 14
  }'
```

### Return a Book
```bash
curl -X POST "http://localhost:8000/loans/1/return"
```

## Technologies

- **FastAPI**: Modern async web framework
- **SQLAlchemy**: ORM for database operations
- **PostgreSQL**: Relational database
- **Pydantic**: Data validation
- **Uvicorn**: ASGI server

## Development

### Running Tests

```bash
pytest
```

### Database Migrations (with Alembic - future enhancement)

```bash
alembic upgrade head
```

## Future Enhancements

- [ ] User authentication and authorization
- [ ] Database migrations with Alembic
- [ ] Unit and integration tests
- [ ] Docker and Docker Compose setup
- [ ] Logging and monitoring
- [ ] Rate limiting
- [ ] Book reviews and ratings
- [ ] Reservation system
- [ ] Fine management system
- [ ] Email notifications

## Author

Created for learning purpose as part of a project-based learning curriculum.
