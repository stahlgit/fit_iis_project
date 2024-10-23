from typing import List, Optional

from sqlalchemy.orm import Session

from app.api.crud.base import CRUD
from app.api.models import Conference
from app.api.v1.schemas.conference import ConferenceCreate, ConferenceUpdate


class CRUDconference(CRUD[Conference, ConferenceCreate, ConferenceUpdate]):
    def get_by_name(self, db: Session, name: str) -> Optional[Conference]:
        return db.query(Conference).filter(Conference.name == name).first()
