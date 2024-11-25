from __future__ import annotations

from typing import Optional

from pydantic import BaseModel

import app.api.v1.schemas as schemas


class GivenPresentationBase(BaseModel):
    proposal: Optional[str] = None
    status: Optional[str] = None
    user_id: int
    conference_id: int


class GivenPresentationCreateSchema(GivenPresentationBase):
    pass


class GivenPresentationUpdateSchema(GivenPresentationBase):
    pass


class GivenPresentationSchema(GivenPresentationBase):
    id: int

    class Config:
        from_attributes = True
