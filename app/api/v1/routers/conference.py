from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api import models
from app.api.crud import conference as CRUDconference  # # TODO nejak to upratat
from app.api.models import Conference
from app.api.v1.schemas import conference as schemas
from app.services.database import get_db

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
        existing_conference = CRUDconference.get_by_name(db, name=conference_in.name)
        if existing_conference:
            raise HTTPException(status_code=400, detail="Conference already registered")
        return await models.Conference.create(db, conference_in)
    except Exception as e:
        raise HTTPException(400, f"Error occurred: {e}")


@router.get("/all", response_model=List[schemas.ConferenceCreate])
async def read_conferences(
    skip: int = 0, limit: int = 100, db: Session = Depends(get_db)
):
    try:
        return await models.Conference.get_all(db)
    except Exception as e:
        raise HTTPException(400, f"Error occurred: {e}")


@router.get("/{conference_id}", response_model=schemas.ConferenceCreate)
async def read_conference(conference_id: int, db: Session = Depends(get_db)):
    try:
        conference = await models.Conference.get(db, id=conference_id)
        return await conference
    except conference.DoesNotExist:
        raise HTTPException(status_code=404, detail="Conference not found")
    except Exception as e:
        raise HTTPException(400, f"Error occurred: {e}")


@router.put("/{conference_id}", response_model=schemas.ConferenceUpdate)
async def update_conference(
    conference_id: int,
    conference_in: schemas.ConferenceUpdate,
    db: Session = Depends(get_db),
):
    try:
        conference = await models.Conference.get(db, id=conference_id)
        if conference is None:
            raise HTTPException(status_code=404, detail="Conference not found")
        conference = await models.Conference.update(
            db, id=conference_id, **conference_in.model_dump()
        )
        await db.commit()  # a tak pre istotu asi xddd
        await db.refresh(conference)
        return conference

    except Exception as e:
        raise HTTPException(400, f"Error occurred: {e}")


@router.delete("/{conference_id}", response_model=schemas.ConferenceCreate)
async def delete_conference(conference_id: int, db: Session = Depends(get_db)):
    try:
        conference = await models.Conference.get(db, id=conference_id)
        if conference is None:
            raise HTTPException(status_code=404, detail="Conference not found")

        await models.Conference.delete(db, id=conference_id)
        await db.commit()
        return conference  # Returning the deleted conference for consistency (optional)
    except Exception as e:
        raise HTTPException(400, f"Error occurred: {e}")
