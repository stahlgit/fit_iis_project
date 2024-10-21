from typing import List, Optional

from sqlalchemy.orm import Session

from app.api.models import Conference
from app.api.v1.schemas.conference import (
    ConferenceCreate,
    ConferenceRead,
    ConferenceUpdate,
)


class CRUDConference:
    def get(self, db: Session, id: int) -> Optional[Conference]:
        return db.query(Conference).filter(Conference.id == id).first()

    def get_multi(
        self, db: Session, skip: int = 0, limit: int = 100
    ) -> List[Conference]:
        return db.query(Conference).offset(skip).limit(limit).all()

    def create(self, db: Session, conference: ConferenceCreate) -> Conference:
        db_conference = Conference(
            name=conference.name,
            description=conference.description,
            genre=conference.genre,
            place=conference.place,
            time_interval=conference.time_interval,
            price=conference.price,
            capacity=conference.capacity,
        )
        db.add(db_conference)
        db.commit()
        db.refresh(db_conference)
        return db_conference

    def update(
        self, db: Session, conference: Conference, conference_in: ConferenceUpdate
    ) -> Conference:
        conference_data = conference.dict()
        update_data = conference_in.dict(exclude_unset=True)
        for field in conference_data:
            if field in update_data:
                setattr(conference, field, update_data[field])
        db.add(conference)
        db.commit()
        db.refresh(conference)
        return conference

    def delete(self, db: Session, id: int) -> Conference:
        conference = db.query(Conference).get(id)
        db.delete(conference)
        db.commit()
        return conference

    def get_conference_by_name(self, db: Session, name: str) -> Conference:
        return db.query(Conference).filter(Conference.name == name).first()
