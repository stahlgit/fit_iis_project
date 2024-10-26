from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Session

from app.api.models import Reservation
from app.api.v1.schemas import reservation as schemas
from app.services.database import get_db
from app.services.utils import not_found

router = APIRouter(
    prefix="/reservation",
    tags=["reservation"],
    responses={404: {"description": "Not found"}},
)


@router.post(
    "/", response_model=schemas.ReservationSchema, status_code=status.HTTP_201_CREATED
)
async def create_reservation(
    reservation_in: schemas.ReservationCreateSchema, db: Session = Depends(get_db)
):
    try:
        return await Reservation.create(db, reservation_in)
    except Exception as e:
        raise HTTPException(400, f"Error occured: {e}")


@router.get("/all", response_model=List[schemas.ReservationSchema])
async def read_reservations(db: Session = Depends(get_db)):
    try:
        return await Reservation.get_all(db)
    except Exception as e:
        raise HTTPException(400, f"Error occured: {e}")


@router.get("/{reservation_id}", response_model=schemas.ReservationSchema)
async def read_reservation(reservation_id: int, db: AsyncSession = Depends(get_db)):
    try:
        reservation = Reservation.get(db, id=reservation_id)
        return await reservation
    except reservation.DoesNotExist:
        not_found("Reservation")
    except Exception as e:
        raise HTTPException(400, f"Error occured: {e}")


@router.put("/{reservation_id}", response_model=schemas.ReservationUpdateSchema)
async def update_reservation(
    reservation_id: int,
    reservation_in: schemas.ReservationUpdateSchema,
    db: Session = Depends(get_db),
):
    try:
        reservation = Reservation.get(db, id=reservation_id)
        if reservation is None:
            not_found("Reservation")
        return await Reservation.update(
            db, id=reservation_id, **reservation_in.model_dump()
        )
    except Exception as e:
        raise HTTPException(400, f"Error occurred: {e}")


@router.delete("/{reservation_id}")
async def delete_reservation(reservation_id: int, db: Session = Depends(get_db)):
    try:
        reservation = await Reservation.get(db, id=reservation_id)
        if reservation is None:
            not_found("Reservation")
        await Reservation.delete(db, id=reservation_id)
        return reservation
    except Exception as e:
        raise HTTPException(400, f"Error occurred: {e}")
