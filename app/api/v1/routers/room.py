from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.models import Room
from app.api.v1.schemas import room as schemas
from app.services.database import get_db
from app.services.logging import log_endpoint
from app.services.utils import not_found

router = APIRouter(
    prefix="/room",
    tags=["room"],
    responses={404: {"description": "Not found"}},
)


@router.post(
    "/", response_model=schemas.RoomSchema, status_code=status.HTTP_201_CREATED
)
@log_endpoint
async def create_room(room_in: schemas.RoomCreateSchema, db: Session = Depends(get_db)):
    try:
        if await Room.get_by(db, name=room_in.name):
            raise HTTPException(status_code=400, detail="Room already registered")
        return await Room.create(db, **room_in.model_dump())
    except Exception as e:
        raise HTTPException(400, f"Error occured: {e}")


@router.get("/all", response_model=List[schemas.RoomSchema])
@log_endpoint
async def read_rooms(db: Session = Depends(get_db)):
    try:
        return await Room.get_all(db)
    except Exception as e:
        raise HTTPException(400, f"Error occured: {e}")


@router.get("/{room_id}", response_model=schemas.RoomSchema)
@log_endpoint
async def read_room(room_id: int, db: Session = Depends(get_db)):
    try:
        room = await Room.get(room_id, session=db)
        if not room:
            not_found("Room")
        return schemas.RoomSchema(**room.__dict__)
    except Exception as e:
        raise HTTPException(400, f"Error occured: {e}")


@router.put("/{room_id}", response_model=schemas.RoomUpdateSchema)
@log_endpoint
async def update_room(
    room_id: int, room_in: schemas.RoomUpdateSchema, db: Session = Depends(get_db)
):
    try:
        room = await Room.get(room_id, session=db)
        if not room:
            not_found("Room")
        return await Room.update(db, id=room_id, **room_in.model_dump())
    except Exception as e:
        raise HTTPException(400, f"Error occurred: {e}")


@router.delete("/{room_id}")
@log_endpoint
async def delete_room(room_id: int, db: Session = Depends(get_db)):
    try:
        room = await Room.get(room_id, session=db)
        if room is None:
            not_found("Room")
        await Room.delete(db, id=room_id)
        return room
    except Exception as e:
        raise HTTPException(400, f"Error occurred: {e}")
