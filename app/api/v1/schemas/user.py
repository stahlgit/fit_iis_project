from __future__ import annotations

from enum import Enum
from typing import List, Optional

from pydantic import BaseModel

from app.api.models import UserRole
from app.api.v1 import schemas as schemas


class TokenData(BaseModel):
    id: int | None = None


class Token(BaseModel):
    access_token: str
    token_type: str


class UserBase(BaseModel):
    name: str
    email: str


class UserCreate(UserBase):
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


class Token(BaseModel):
    access_token: str
    token_type: str
