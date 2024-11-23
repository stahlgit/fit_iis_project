from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.crud import ticket as crud
from app.api.crud.user import role_required
from app.api.models import Ticket, User, UserRole
from app.api.v1.schemas import ticket as schemas
from app.services import get_db, log_endpoint, not_found

router = APIRouter(
    prefix="/ticket",
    tags=["ticket"],
    responses={404: {"description": "Not found"}},
)


@router.post(
    "/", response_model=schemas.TicketSchema, status_code=status.HTTP_201_CREATED
)
@log_endpoint
async def create_ticket(
    ticket_in: schemas.TicketCreateSchema,
    db: Session = Depends(get_db),
    current_user: User = Depends(role_required(UserRole.REGISTERED)),
) -> schemas.TicketSchema:
    try:
        ticket = await crud.create_ticket(db=db, ticket_in=ticket_in)
        return ticket
    except Exception as e:
        raise HTTPException(400, f"Error occured: {e}")


@router.get("/all", response_model=List[schemas.TicketSchema])
@log_endpoint
async def read_tickets(
    db: Session = Depends(get_db),
    current_user: User = Depends(role_required(UserRole.REGISTERED)),
) -> List[schemas.TicketSchema]:
    try:
        return await Ticket.get_all(db)
    except Exception as e:
        raise HTTPException(400, f"Error occured: {e}")


@router.get("/{ticket_id}", response_model=schemas.TicketSchema)
@log_endpoint
async def read_ticket(
    ticket_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(role_required(UserRole.REGISTERED)),
) -> schemas.TicketSchema:
    try:
        ticket = Ticket.get_by(ticket_id, session=db)
        if not ticket:
            not_found("Ticket")
        return schemas.TicketSchema(**ticket.__dict__)
    except Exception as e:
        raise HTTPException(400, f"Error occured: {e}")


@router.put("/{ticket_id}", response_model=schemas.TicketUpdateSchema)
@log_endpoint
async def update_ticket(
    ticket_id: int,
    ticket_in: schemas.TicketUpdateSchema,
    db: Session = Depends(get_db),
    current_user: User = Depends(role_required(UserRole.REGISTERED)),
) -> schemas.TicketUpdateSchema:
    try:
        ticket = Ticket.get(ticket_id, session=db)
        if not ticket:
            not_found("Ticket")
        return await Ticket.update(db, id=ticket_id, **ticket_in.model_dump())
    except Exception as e:
        raise HTTPException(400, f"Error occurred: {e}")


@router.delete("/{ticket_id}", response_model=schemas.TicketSchema)
@log_endpoint
async def delete_ticket(
    ticket_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(role_required(UserRole.REGISTERED)),
):
    try:
        ticket = Ticket.get(ticket_id, session=db)
        if not ticket:
            not_found("Ticket")
        await Ticket.delete(db, id=ticket_id)
        return ticket
    except Exception as e:
        raise HTTPException(400, f"Error occurred: {e}")
