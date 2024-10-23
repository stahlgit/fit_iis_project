from typing import List, Optional

from pydantic import BaseModel

# TODO import reservation schema


class UserBase(BaseModel):
    name: str
    email: str
    role: str  # TODO ENUM


class UserCreate(UserBase):
    password: str


class UserUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[str] = None
    role: Optional[str] = None
    password: Optional[str] = None  # Allow password update


class UserRead(UserBase):
    id: int
    # TODO RESEVATION LIST

    class Config:
        orm_mode = True


class Users(BaseModel):
    __root__: List[UserRead]
