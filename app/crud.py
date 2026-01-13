from sqlalchemy.orm import Session
from . import models, schemas, auth

# User CRUD
def get_user_by_username(db: Session, username: str):
    return db.query(models.User).filter(models.User.username == username).first()

def create_user(db: Session, user: schemas.UserCreate):
    hashed_password = auth.get_password_hash(user.password)
    db_user = models.User(username=user.username, password_hash=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

# Employee CRUD
def get_employee(db: Session, employee_id: int):
    return db.query(models.Employee).filter(models.Employee.id == employee_id).first()

def get_employee_by_email(db: Session, email: str):
    return db.query(models.Employee).filter(models.Employee.email == email).first()

def get_employees(db: Session, skip: int = 0, limit: int = 10, department: str = None, role: str = None):
    query = db.query(models.Employee)
    if department:
        query = query.filter(models.Employee.department == department)
    if role:
        query = query.filter(models.Employee.role == role)
    
    total = query.count()
    items = query.offset(skip).limit(limit).all()
    return items, total

def create_employee(db: Session, employee: schemas.EmployeeCreate):
    db_employee = models.Employee(**employee.model_dump())
    db.add(db_employee)
    db.commit()
    db.refresh(db_employee)
    return db_employee

def update_employee(db: Session, db_employee: models.Employee, employee: schemas.EmployeeUpdate):
    update_data = employee.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_employee, key, value)
    db.commit()
    db.refresh(db_employee)
    return db_employee

def delete_employee(db: Session, db_employee: models.Employee):
    db.delete(db_employee)
    db.commit()
    return True
