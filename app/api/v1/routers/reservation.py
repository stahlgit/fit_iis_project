from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Session

from app.api.models import Reservation
from app.api.v1.schemas import reservation as schemas
from app.services.database import get_db
from app.services.logging import log_endpoint
from app.services.utils import not_found

router = APIRouter(
    prefix="/reservation",
    tags=["reservation"],
    responses={404: {"description": "Not found"}},
)


@router.post(
    "/", response_model=schemas.ReservationSchema, status_code=status.HTTP_201_CREATED
)
@log_endpoint
async def create_reservation(
    reservation_in: schemas.ReservationCreateSchema, db: Session = Depends(get_db)
):
    try:
        if await Reservation.get_by(db, name=reservation_in.name):
            raise HTTPException(
                status_code=400, detail="Reservation already registered"
            )
        return await Reservation.create(db, **reservation_in.model_dump())
    except Exception as e:
        raise HTTPException(400, f"Error occured: {e}")


@router.get("/all", response_model=List[schemas.ReservationSchema])
@log_endpoint
async def read_reservations(db: Session = Depends(get_db)):
    try:
        return await Reservation.get_all(db)
    except Exception as e:
        raise HTTPException(400, f"Error occured: {e}")


@router.get("/{reservation_id}", response_model=schemas.ReservationSchema)
@log_endpoint
async def read_reservation(reservation_id: int, db: AsyncSession = Depends(get_db)):
    try:
        reservation = await Reservation.get(reservation_id, session=db)
        if not reservation:
            not_found("Reservation")
        return schemas.ReservationSchema(**reservation.__dict__)
    except Exception as e:
        raise HTTPException(400, f"Error occured: {e}")


@router.put("/{reservation_id}", response_model=schemas.ReservationUpdateSchema)
@log_endpoint
async def update_reservation(
    reservation_id: int,
    reservation_in: schemas.ReservationUpdateSchema,
    db: Session = Depends(get_db),
):
    try:
        reservation = await Reservation.get(reservation_id, session=db)
        if not reservation:
            not_found("Reservation")
        return Reservation.update(db, id=reservation_id, **reservation_in.model_dump())
    except Exception as e:
        raise HTTPException(400, f"Error occurred: {e}")


@router.delete("/{reservation_id}")
@log_endpoint
async def delete_reservation(reservation_id: int, db: Session = Depends(get_db)):
    try:
        reservation = await Reservation.get(reservation_id, session=db)
        if not reservation:
            not_found("Reservation")
        await Reservation.delete(db, id=reservation_id)
        return reservation
    except Exception as e:
        raise HTTPException(400, f"Error occurred: {e}")
