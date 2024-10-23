from typing import List, Optional

from sqlalchemy.orm import Session

from app.api.models import Conference
from app.api.v1.schemas.conference import ConferenceCreate, ConferenceUpdate


async def get_by_name(db: Session, name: str) -> Optional[Conference]:
    return db.query(Conference).filter(Conference.name == name).first()


async def search_conferences(
    db: Session, *, keyword: str, skip: int = 0, limit: int = 100
) -> List[Conference]:
    return (
        db.query(Conference)
        .filter(Conference.name.contains(keyword))
        .offset(skip)
        .limit(limit)
        .all()
    )