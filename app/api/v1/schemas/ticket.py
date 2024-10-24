from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, Field

from app.api.v1 import schemas as schemas


class TicketBase(BaseModel):
    created_at: datetime = Field(default_factory=datetime.now)
    reservation_id: int


class TicketCreateSchema(TicketBase):
    pass


class TicketUpdateSchema(TicketBase):
    # maybe not ?
    pass


class TicketSchema(TicketBase):
    id: int
    # reservation: schemas.ReservationSchema

    class Config:
        from_attributes = True
