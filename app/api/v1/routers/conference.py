from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.models import Conference
from app.api.v1.schemas import conference as schemas
from app.services.database import get_db
from app.services.utils import not_found

router = APIRouter(
    prefix="/conferences",
    tags=["conferences"],
    responses={404: {"description": "Not found"}},
)


@router.post(
    "/", response_model=schemas.ConferenceCreate, status_code=status.HTTP_201_CREATED
)
async def create_conference(
    conference_in: schemas.ConferenceCreate, db: Session = Depends(get_db)
):
    try:
        if await Conference.get_by(db, name=conference_in.name):
            raise HTTPException(status_code=400, detail="Conference already registered")
        return await Conference.create(db, **conference_in.model_dump())
    except Exception as e:
        raise HTTPException(400, f"Error occurred: {e}")


@router.get("/all", response_model=List[schemas.ConferenceSchema])
async def read_conferences(db: Session = Depends(get_db)):  # TODO skip + limit
    try:
        return await Conference.get_all(db)
    except Exception as e:
        raise HTTPException(400, f"Error occurred: {e}")


@router.get("/{conference_id}", response_model=schemas.ConferenceSchema)
async def read_conference(conference_id: int, db: Session = Depends(get_db)):
    try:
        conference = await Conference.get(conference_id, session=db)
        if not conference:
            not_found("Conference")
        return schemas.ConferenceSchema(**conference.__dict__)

    except Exception as e:
        raise HTTPException(400, f"Error occurred: {e}")


@router.put("/{conference_id}", response_model=schemas.ConferenceUpdate)
async def update_conference(
    conference_id: int,
    conference_in: schemas.ConferenceUpdate,
    db: Session = Depends(get_db),
):
    try:
        conference = await Conference.get(conference_id, session=db)
        if not conference:
            not_found("Conference")
        return await Conference.update(
            db, id=conference_id, **conference_in.model_dump()
        )
    except Exception as e:
        raise HTTPException(400, f"Error occurred: {e}")


@router.delete("/{conference_id}")
async def delete_conference(conference_id: int, db: Session = Depends(get_db)):
    try:
        conference = await Conference.get(conference_id, session=db)
        if not conference:
            not_found("Conference")
        await Conference.delete(db, id=conference_id)
        return conference
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error occurred: {e}")
