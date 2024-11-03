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
        existing_conference = await Conference.get_by(db, name=conference_in.name)
        if existing_conference:
            raise HTTPException(status_code=400, detail="Conference already registered")
        return await Conference.create(db, **conference_in.model_dump())
    except Exception as e:
        raise HTTPException(400, f"Error occurred: {e}")


@router.get("/all", response_model=List[schemas.ConferenceCreate])
async def read_conferences(db: Session = Depends(get_db)):  # TODO skip + limit
    try:
        return await Conference.get_all(db)
    except Exception as e:
        raise HTTPException(400, f"Error occurred: {e}")


@router.get("/{conference_id}", response_model=schemas.ConferenceCreate)
async def read_conference(conference_id: int, db: Session = Depends(get_db)):
    try:
        conference = Conference.get(db, id=conference_id)
        return await conference
    except conference.DoesNotExist:
        not_found("Conference")
    except Exception as e:
        raise HTTPException(400, f"Error occurred: {e}")


@router.put("/{conference_id}", response_model=schemas.ConferenceUpdate)
async def update_conference(
    conference_id: int,
    conference_in: schemas.ConferenceUpdate,
    db: Session = Depends(get_db),
):
    try:
        conference = await Conference.get(db, id=conference_id)
        if conference is None:
            not_found("Conference")
        conference = await Conference.update(
            db, id=conference_id, **conference_in.model_dump()
        )
        await db.commit()  # a tak pre istotu asi xddd
        await db.refresh(conference)
        return conference

    except Exception as e:
        raise HTTPException(400, f"Error occurred: {e}")


@router.delete("/{conference_id}")
async def delete_conference(conference_id: int, db: Session = Depends(get_db)):
    try:
        conference = await Conference.get(db, id=conference_id)
        if conference is None:
            not_found("Conference")

        await Conference.delete(db, id=conference_id)
        await db.commit()
        return conference  # Returning the deleted conference for consistency (optional)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error occurred: {e}")
