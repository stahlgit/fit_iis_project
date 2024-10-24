from typing import List, Optional

from pydantic import BaseModel
from sqlalchemy.dialects.postgresql import TSTZRANGE

import app.api.v1.schemas as schemas


class LectureBase(BaseModel):
    name: str
    description: Optional[str] = None
    time_interval: Optional[TSTZRANGE] = None
    tags: Optional[str] = None
    image: Optional[str] = None
    room_id: int
    conference_id: int
    lecturer_id: int


class LectureCreateSchema(LectureBase):
    pass


class LectureUpdateSchema(LectureBase):
    pass


class LectureSchema(LectureBase):
    id: int
    room: schemas.RoomSchema
    conference: schemas.ConferenceSchema
    lecturer: schemas.UserSchema
    voting: List[schemas.VotingSchema] = []
    questions: List[schemas.QuestionSchema] = []

    class Config:
        orm_mode = True
