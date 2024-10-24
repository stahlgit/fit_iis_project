from __future__ import annotations

from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel

from app.api.v1 import schemas as schemas


class ConferenceBase(BaseModel):
    name: str
    description: Optional[str] = None
    genre: Optional[str] = None
    place: Optional[str] = None
    time_interval: Optional[tuple[datetime, datetime]] = None
    price: Optional[float] = None
    capacity: Optional[int] = None

    model_config = {"arbitrary_types_allowed": True}


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


class ConferenceSchema(ConferenceBase):
    id: int

    class Config:
        from_attributes = True
