from fastapi import FastAPI, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm
from datetime import timedelta
from typing import Optional

from . import models, schemas, crud, auth, database
from .database import engine, get_db

# Create database tables
models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Employee Management API")

@app.get("/")
def root():
    return {"status": "API is running"}

# Default admin user setup
@app.on_event("startup")
def startup_populate_db():
    db = next(get_db())
    # Create default admin if not exists
    admin_user = crud.get_user_by_username(db, "admin")
    if not admin_user:
        crud.create_user(db, schemas.UserCreate(username="admin", password="password123"))
        print("Default admin user created: admin/password123")

# --- Auth Endpoints ---

@app.post("/api/auth/token", response_model=schemas.Token)
def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = crud.get_user_by_username(db, form_data.username)
    if not user or not auth.verify_password(form_data.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=auth.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = auth.create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

# --- Employee Endpoints ---

@app.post("/api/employees/", response_model=schemas.EmployeeRead, status_code=status.HTTP_201_CREATED)
def create_employee(
    employee: schemas.EmployeeCreate, 
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_user)
):
    db_employee = crud.get_employee_by_email(db, email=employee.email)
    if db_employee:
        raise HTTPException(status_code=400, detail="Employee with this email already exists")
    return crud.create_employee(db=db, employee=employee)

@app.get("/api/employees/", response_model=schemas.EmployeeList)
def list_employees(
    page: int = Query(1, ge=1),
    department: Optional[str] = None,
    role: Optional[str] = None,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_user)
):
    size = 10
    skip = (page - 1) * size
    items, total = crud.get_employees(db, skip=skip, limit=size, department=department, role=role)
    return {
        "items": items,
        "total": total,
        "page": page,
        "size": size
    }

@app.get("/api/employees/{employee_id}", response_model=schemas.EmployeeRead)
def read_employee(
    employee_id: int, 
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_user)
):
    db_employee = crud.get_employee(db, employee_id=employee_id)
    if db_employee is None:
        raise HTTPException(status_code=404, detail="Employee not found")
    return db_employee

@app.put("/api/employees/{employee_id}", response_model=schemas.EmployeeRead)
def update_employee(
    employee_id: int, 
    employee: schemas.EmployeeUpdate, 
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_user)
):
    db_employee = crud.get_employee(db, employee_id=employee_id)
    if db_employee is None:
        raise HTTPException(status_code=404, detail="Employee not found")
    return crud.update_employee(db=db, db_employee=db_employee, employee=employee)

@app.delete("/api/employees/{employee_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_employee(
    employee_id: int, 
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_user)
):
    db_employee = crud.get_employee(db, employee_id=employee_id)
    if db_employee is None:
        raise HTTPException(status_code=404, detail="Employee not found")
    crud.delete_employee(db=db, db_employee=db_employee)
    return None
