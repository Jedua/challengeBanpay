from pydantic import BaseModel, EmailStr, ConfigDict, Field
from enum import Enum
from typing import Optional

# Roles obligatorios según el requerimiento 
class UserRole(str, Enum):
    ADMIN = "admin"
    FILMS = "films"
    PEOPLE = "people"
    LOCATIONS = "locations"
    SPECIES = "species"
    VEHICLES = "vehicles"

class UserBase(BaseModel):
    username: str = Field(..., min_length=3, max_length=50)
    email: EmailStr
    role: UserRole

class UserCreate(UserBase):
    password: str = Field(..., min_length=8)

class UserUpdate(BaseModel):
    username: Optional[str] = Field(None, min_length=3, max_length=50)
    email: Optional[EmailStr] = None
    password: Optional[str] = Field(None, min_length=8)
    role: Optional[UserRole] = None
    
class UserUpdateMe(BaseModel):
    username: Optional[str] = None
    email: Optional[EmailStr] = None
    password: Optional[str] = None

class User(UserBase):
    id: int
    
    # Permite la compatibilidad con modelos de SQLAlchemy
    model_config = ConfigDict(from_attributes=True)