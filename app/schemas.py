from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import date

# User Schemas
class UserBase(BaseModel):
    username: str

class UserCreate(UserBase):
    password: str

class UserLogin(UserBase):
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None

# Employee Schemas
class EmployeeBase(BaseModel):
    name: str = Field(..., min_length=1)
    email: EmailStr
    department: Optional[str] = None
    role: Optional[str] = None

class EmployeeCreate(EmployeeBase):
    pass

class EmployeeUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1)
    email: Optional[EmailStr] = None
    department: Optional[str] = None
    role: Optional[str] = None

class EmployeeRead(EmployeeBase):
    id: int
    date_joined: date

    class Config:
        from_attributes = True

class EmployeeList(BaseModel):
    items: list[EmployeeRead]
    total: int
    page: int
    size: int
