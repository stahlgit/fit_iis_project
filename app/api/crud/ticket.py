from sqlalchemy.orm import Session

from app.api.models import Reservation, Ticket
from app.api.v1.schemas.ticket import TicketCreateSchema


async def create_ticket(db: Session, ticket_in: TicketCreateSchema):
    reservation = await Reservation.get_one_by(db, id=ticket_in.reservation_id)
    if not reservation:
        raise Exception("Reservation not found")
    print(reservation.id)
    reservation.number_of_tickets += 1
    await Reservation.update(
        db, id=reservation.id, number_of_tickets=reservation.number_of_tickets
    )

    ticket = await Ticket.create(db, **ticket_in.model_dump())
    return ticket
