from __future__ import annotations

from typing import List, Optional

from pydantic import BaseModel

from app.api.models import Room
from app.api.v1 import schemas as schemas


class RoomBase(BaseModel):
    name: str
    capacity: Optional[int]
    conference_id: Optional[int] = None


class RoomCreateSchema(RoomBase):
    pass


class RoomUpdateSchema(RoomBase):
    pass


class RoomSchema(RoomBase):
    id: int

    class Config:
        from_attributes = True
