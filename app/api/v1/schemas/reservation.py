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
    pass


class ReservationUpdateSchema(ReservationBase):
    pass


class ReservationSchema(ReservationBase):
    id: int
    user: Optional[schemas.UserSchema] = None
    conference: schemas.ConferenceSchema
    tickets: List[schemas.TicketSchema] = []

    class Config:
        orm_mode = True
