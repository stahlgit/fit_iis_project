from typing import List, Optional

from sqlalchemy.orm import Session

from app.api.models import Conference
from app.api.v1.schemas.conference import ConferenceCreate, ConferenceUpdate


async def search_conferences(
    db: Session, *, keyword: str, skip: int = 0, limit: int = 100
) -> List[Conference]:
    return await (
        db.query(Conference)
        .filter(Conference.name.contains(keyword))
        .offset(skip)
        .limit(limit)
        .all()
    )
