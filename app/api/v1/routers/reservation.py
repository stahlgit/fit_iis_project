from typing import List, Union

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Session

from app.api.crud.user import create_guest
from app.api.models import Conference, Reservation, User
from app.api.v1.schemas import reservation as schemas
from app.api.v1.schemas.user import UserSchema
from app.services import check_entities_exist, get_db, log_endpoint, not_found

router = APIRouter(
    prefix="/reservation",
    tags=["reservation"],
    responses={404: {"description": "Not found"}},
)


@router.post("/", status_code=status.HTTP_201_CREATED)
@log_endpoint
async def create_reservation(
    reservation_in: schemas.ReservationCreateSchema,
    db: Session = Depends(get_db),
) -> schemas.ReservationSchema:
    try:
        await check_entities_exist(
            db,
            {
                "conference": [reservation_in.conference_id],
            },
        )

        if reservation_in.user_id is not None:
            user = await User.get(reservation_in.user_id, session=db)
            if not user:
                not_found("User")
            reservation_data = reservation_in.model_dump()
            reservation_data.pop("email")

            reservation = await Reservation.create(db, **reservation_data)
            return schemas.ReservationSchema.from_orm(reservation)
        else:
            guest = await create_guest(db, reservation_in.email)

            reservation_data = reservation_in.model_dump()
            reservation_data.pop("email")
            reservation_data["user_id"] = guest.id

            reservation = await Reservation.create(db, **reservation_data)
            return schemas.ReservationGuestSchema(
                number_of_tickets=reservation.number_of_tickets,
                status=reservation.status,
                paid=reservation.paid,
                user_id=guest.id,
                conference_id=reservation.conference_id,
                username=guest.name,
                email=guest.email,
                password=guest.name,  ##username == password
            )

    except Exception as e:
        raise HTTPException(400, f"Error occured: {e}")


@router.get("/all", response_model=List[schemas.ReservationSchema])
@log_endpoint
async def read_reservations(
    db: Session = Depends(get_db),
) -> List[schemas.ReservationSchema]:
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
