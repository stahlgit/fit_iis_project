from __future__ import annotations

from typing import List, Optional

from pydantic import BaseModel

from app.api.v1 import schemas as schemas


class ReservationBase(BaseModel):
    number_of_tickets: int
    status: Optional[str] = None
    paid: bool
    user_id: Optional[int] = None
    conference_id: int


class ReservationCreateSchema(ReservationBase):
    email: Optional[str] = None  ## guest


class ReservationUpdateSchema(ReservationBase):
    pass


class ReservationSchema(ReservationBase):
    id: int

    class Config:
        from_attributes = True


class ReservationGuestSchema(ReservationBase):
    id: int

    class Config:
        from_attributes = True
