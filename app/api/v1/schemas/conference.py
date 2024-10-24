from typing import List, Optional

from pydantic import BaseModel
from sqlalchemy.dialects.postgresql import TSTZRANGE

from app.api.v1 import schemas as schemas


class ConferenceBase(BaseModel):
    name: str
    description: Optional[str] = None
    genre: Optional[str] = None
    place: Optional[str] = None
    time_interval: Optional[TSTZRANGE] = None
    price: Optional[float] = None
    capacity: Optional[int] = None


class ConferenceCreate(ConferenceBase):
    pass


class ConferenceUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    genre: Optional[str] = None
    place: Optional[str] = None
    time_interval: Optional[str] = None
    price: Optional[float] = None
    capacity: Optional[int] = None


class ConferenceRead(ConferenceBase):
    id: int
    rooms: List[
        schemas.RoomSchema
    ] = []  # or we could update this for RoomReadSchema --> specific things for reading
    lectures: List[schemas.LectureSchema] = []

    class Config:
        from_attributes = True


class ConferenceSchema(ConferenceBase):
    id: int
    rooms: List[schemas.RoomSchema] = []
    lectures: List[schemas.LectureSchema] = []
    reservations: List[schemas.ReservationSchema] = []
    given_presentations: List[schemas.GivenPresentationSchema] = []

    class Config:
        orm_mode = True
