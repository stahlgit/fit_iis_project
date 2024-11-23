from __future__ import annotations

from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel

import app.api.v1.schemas as schemas


class LectureBase(BaseModel):
    name: str
    description: Optional[str] = None
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None
    tags: Optional[str] = None
    image: Optional[str] = None
    room_id: int
    conference_id: int
    lecturer_id: int

    model_config = {"arbitrary_types_allowed": True}


class LectureCreateSchema(LectureBase):
    pass


class LectureUpdateSchema(LectureBase):
    pass


class LectureSchema(LectureBase):
    id: int

    class Config:
        from_attributes = True
