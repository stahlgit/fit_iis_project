from __future__ import annotations

from pydantic import BaseModel

import app.api.v1.schemas as schemas


class QuestionBase(BaseModel):
    text: str
    user_id: int
    lecture_id: int


class QuestionCreateSchema(QuestionBase):
    pass


class QuestionUpdateSchema(QuestionBase):
    pass


class QuestionSchema(QuestionBase):
    id: int

    class Config:
        from_attributes = True
