from __future__ import annotations

from enum import Enum
from typing import List, Optional

from pydantic import BaseModel, EmailStr

from app.api.v1 import schemas as schemas


class UserRoleEnum(str, Enum):
    ADMIN = "admin"
    REGISTERED = "registered"
    GUEST = "guest"


class UserBase(BaseModel):
    name: str
    email: str
    role: UserRoleEnum = UserRoleEnum.GUEST


class UserCreate(UserBase):
    name: str
    email: EmailStr
    password: Optional[str] = None


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class UserUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[str] = None
    role: Optional[str] = None
    password: Optional[str] = None  # Allow password update


class UserRead(UserBase):
    id: int
    reservation: List[schemas.ReservationSchema]

    class Config:
        from_attributes = True


# class Users(BaseModel):
# __root__: List[UserRead]


class UserSchema(UserBase):
    id: int

    class Config:
        from_attributes = True
