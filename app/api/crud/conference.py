from typing import List, Optional

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.api.models import Conference, Reservation
from app.api.v1.schemas import ConferenceAvailableSpaces
from app.services.utils import not_found


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


async def get_free_tickets(conference: Conference, db: Session):
    try:
        # Calculate total reserved tickets for the conference
        total_reserved_tickets = (
            await db.execute(
                select(func.sum(Reservation.number_of_tickets)).filter(
                    Reservation.conference_id == conference.id
                )
            )
        ).scalar() or 0  # Default to 0 if no reservations exist
        # Calculate available spaces
        available_spaces = conference.capacity - total_reserved_tickets

        return ConferenceAvailableSpaces(available=available_spaces)

    except Exception as e:
        raise Exception(f"Error occurred: {e}")
