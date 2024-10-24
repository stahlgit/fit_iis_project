from enum import Enum
from typing import List, Optional

from pydantic import BaseModel

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
        orm_mode = True


class Users(BaseModel):
    __root__: List[UserRead]


class UserSchema(UserBase):
    id: int
    lectures: List[schemas.LectureSchema] = []
    voting: List[schemas.VotingSchema] = []
    questions: List[schemas.QuestionSchema] = []
    reservations: List[schemas.ReservationSchema] = []
    given_presentations: List[schemas.GivenPresentationSchema] = []

    class Config:
        orm_mode = True
