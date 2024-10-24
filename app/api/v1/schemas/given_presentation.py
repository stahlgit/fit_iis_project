from typing import Optional

from pydantic import BaseModel

import app.api.v1.schemas as schemas


class GivenPresentationBase(BaseModel):
    proposal: Optional[str] = None
    status: str
    user_id: int
    conference_id: int


class GivenPresentationCreateSchema(GivenPresentationBase):
    pass


class GivenPresentationUpdateSchema(GivenPresentationBase):
    pass


class GivenPresentationSchema(GivenPresentationBase):
    id: int
    user: schemas.UserSchema
    conference: schemas.ConferenceSchema

    class Config:
        orm_more = True
