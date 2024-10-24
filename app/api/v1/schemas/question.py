from pydantic import BaseModel

import app.api.v1.schemas as schemas


class QuestionBase(BaseModel):
    text: str
    user_id: int
    lecture_id: int


class QuestionCreateSchema(QuestionBase):
    pass


class QuestionSchema(QuestionBase):
    id: int
    user: schemas.UserSchema
    lecture: schemas.LectureSchema

    class Config:
        orm_mode = True
