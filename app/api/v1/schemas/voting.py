from __future__ import annotations

from pydantic import BaseModel, Field

import app.api.v1.schemas as schemas


class VotingBaseSchema(BaseModel):
    user_id: int
    lecture_id: int
    rating: int = Field(..., ge=1, le=5)


class VotingCreateSchema(VotingBaseSchema):
    pass


class VotingUpdateSchema(VotingBaseSchema):
    pass


class VotingSchema(VotingBaseSchema):
    id: int

    class Config:
        from_attributes = True
