from enum import Enum
from pydantic import BaseModel
from typing import Optional

class UserRole(str, Enum):
    EMPLOYEE = "employee"
    ADMIN = "admin"

class User(BaseModel):
    id: int
    username: str
    hashed_password: str
    role: UserRole

class UserCreate(BaseModel):
    username: str
    password: str
    role: UserRole = UserRole.EMPLOYEE

class UserInDB(User):
    pass

class UserResponse(BaseModel):
    id: int
    username: str
    role: UserRole