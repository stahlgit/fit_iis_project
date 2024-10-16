from typing import List, Optional

from pydantic import BaseModel

from app.api.models import Conference


class ConferenceBase(BaseModel):
    name: str
    description: Optional[str] = None
    genre: Optional[str] = None
    place: Optional[str] = None
    time_interval: str  ## TODO TSTZRANGE
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
    rooms: List[RoomRead] = []
    lectures: List[LectureRead] = []

    class Config:
        orm_mode = True


class Conferences(BaseModel):
    __root__: List[ConferenceRead]
