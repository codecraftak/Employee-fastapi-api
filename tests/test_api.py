import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.main import app
from app.database import Base, get_db
import os

# Use an in-memory SQLite database for testing to avoid dependency on a running Postgres
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)

@pytest.fixture(autouse=True, scope="module")
def setup_db():
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    from app import crud, schemas
    admin_user = crud.get_user_by_username(db, "admin")
    if not admin_user:
        crud.create_user(db, schemas.UserCreate(username="admin", password="password123"))
    db.close()
    yield
    Base.metadata.drop_all(bind=engine)

def test_auth_token():
    
    response = client.post(
        "/api/auth/token",
        data={"username": "admin", "password": "password123"}
    )
    assert response.status_code == 200
    assert "access_token" in response.json()

def test_create_employee():
    
    token_response = client.post(
        "/api/auth/token",
        data={"username": "admin", "password": "password123"}
    )
    token = token_response.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    # Create employee
    response = client.post(
        "/api/employees/",
        headers=headers,
        json={
            "name": "John Doe",
            "email": "john@example.com",
            "department": "Engineering",
            "role": "Developer"
        }
    )
    assert response.status_code == 201
    assert response.json()["name"] == "John Doe"

def test_create_duplicate_email():
    token_response = client.post(
        "/api/auth/token",
        data={"username": "admin", "password": "password123"}
    )
    token = token_response.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    # Create duplicate
    response = client.post(
        "/api/employees/",
        headers=headers,
        json={
            "name": "Duplicate User",
            "email": "john@example.com",
            "department": "HR"
        }
    )
    assert response.status_code == 400
    assert "already exists" in response.json()["detail"]

def test_list_employees():
    token_response = client.post(
        "/api/auth/token",
        data={"username": "admin", "password": "password123"}
    )
    token = token_response.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    response = client.get("/api/employees/", headers=headers)
    assert response.status_code == 200
    assert "items" in response.json()
    assert len(response.json()["items"]) >= 1

def test_get_employee_not_found():
    token_response = client.post(
        "/api/auth/token",
        data={"username": "admin", "password": "password123"}
    )
    token = token_response.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    response = client.get("/api/employees/999", headers=headers)
    assert response.status_code == 404
