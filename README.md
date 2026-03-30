# Employee Management REST API

A robust REST API built with FastAPI and PostgreSQL for managing company employees.

## Features
- **CRUD Operations**: Create, List, Retrieve, Update, and Delete employees.
- **Authentication**: JWT-based authentication to secure endpoints.
- **Validation**: Email uniqueness and data validation using Pydantic.
- **Pagination & Filtering**: Efficiently list employees with pagination (10 per page) and filtering by department/role.
- **PostgreSQL**: Robust database management.
- **Swagger Documentation**: Interactive API docs available at `/docs`.

## Tech Stack
- FastAPI
- SQLAlchemy
- PostgreSQL
- JWT (python-jose)
- Pydantic

## Getting Started

### Prerequisites
- Python 3.10+
- PostgreSQL server running locally

### Installation
1. Activate the virtual environment:
   ```powershell
   .\venv\Scripts\activate
   ```
2. Set Environment Variables (Optional, defaults provided):
   ```powershell
   $env:DATABASE_URL="postgresql://postgres:1234@localhost/employee_db"
   $env:SECRET_KEY="your-secret-key"
   ```

### Running the API
Start the server using uvicorn:
```powershell
uvicorn app.main:app --reload
```

## Authentication
A default admin user is created on the first startup:
- **Username**: `admin`
- **Password**: `password123`

To authenticate, send a `POST` request to `/api/auth/token` with `username` and `password` in the body (form-data).

## API Documentation
Once the server is running, visit:
- **Swagger UI**: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
- **ReDoc**: [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc)

## Testing
Run the automated tests using `pytest`:
```powershell
pytest
```
POSTMAN
