from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from requests import Session

from app.api.models import Ticket
from app.api.v1.schemas import ticket as schemas
from app.services.database import get_db
from app.services.utils import not_found

router = APIRouter(
    prefix="ticket",
    tags=["ticket"],
    esponses={404: {"description": "Not found"}},
)


@router.post(
    "/", response_model=schemas.TicketSchema, status_code=status.HTTP_201_CREATED
)
async def create_ticket(
    ticket_in: schemas.TicketCreateSchema, db: Session = Depends(get_db)
):
    try:
        return await Ticket.create(db, ticket_in)
    except Exception as e:
        raise HTTPException(400, f"Error occured: {e}")


@router.get("/all", response_model=List[schemas.TicketSchema])
async def read_tickets(db: Session = Depends(get_db)):
    try:
        return await Ticket.get_all(db)
    except Exception as e:
        raise HTTPException(400, f"Error occured: {e}")


@router.get("/{ticket_id}", response_model=schemas.TicketSchema)
async def read_ticket(ticket_id: int, db: Session = Depends(get_db)):
    try:
        ticket = Ticket.get(db, id=ticket_id)
        return await ticket
    except ticket.DoesNotExist:
        not_found("Ticket")
    except Exception as e:
        raise HTTPException(400, f"Error occured: {e}")


@router.put("/{ticket_id}", response_model=schemas.TicketUpdateSchema)
async def update_ticket(
    ticket_id: int, ticket_in: schemas.TicketUpdateSchema, db: Session = Depends(get_db)
):
    try:
        ticket = Ticket.get(db, id=ticket_id)
        if ticket is None:
            not_found("Ticket")
        return await Ticket.update(db, id=ticket_id, **ticket_in.model_dump())
    except Exception as e:
        raise HTTPException(400, f"Error occurred: {e}")


@router.delete("/{ticket_id}")
async def delete_ticket(ticket_id: int, db: Session = Depends(get_db)):
    try:
        ticket = await Ticket.get(db, id=ticket_id)
        if ticket is None:
            not_found("Ticket")
        await Ticket.delete(db, id=ticket_id)
        return ticket
    except Exception as e:
        raise HTTPException(400, f"Error occurred: {e}")
