from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.crud import conference as crud
from app.api.v1.schemas import conference as schemas
from app.services import get_db

router = APIRouter(
    prefix="/conferences",
    tags=["conferences"],
    responses={404: {"description": "Not found"}},
)

# TODO get current admin user for auth


@router.post(
    "/", response_model=schemas.ConferenceRead, status_code=status.HTTP_201_CREATED
)
def create_conference(
    conference: schemas.ConferenceCreate, db: Session = Depends(get_db)
):
    conference = crud.CRUDConference.get_conference_by_name(db, conference.name)
    if conference:
        raise HTTPException(status_code=400, detail="Conference already registered")
    return crud.CRUDConference.create(db, conference)


@router.get("/", response_model=schemas.Conferences)
def read_conferences(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    conferences = crud.CRUDConference.get_multi(db, skip=skip, limit=limit)
    return conferences


@router.get("/{conference_id}", response_model=schemas.ConferenceRead)
def read_conference(conference_id: int, db: Session = Depends(get_db)):
    conference = crud.CRUDConference.get(db, conference_id)
    if conference is None:
        raise HTTPException(status_code=404, detail="Conference not found")
    return conference


@router.put("/{conference_id}", response_model=schemas.ConferenceRead)
def update_conference(
    conference_id: int,
    conference: schemas.ConferenceUpdate,
    db: Session = Depends(get_db),
):
    db_conference = crud.CRUDConference.get(db, conference_id)
    if db_conference is None:
        raise HTTPException(status_code=404, detail="Conference not found")
    return crud.CRUDConference.update(db, db_conference, conference)


@router.delete("/{conference_id}", response_model=schemas.ConferenceRead)
def delete_conference(conference_id: int, db: Session = Depends(get_db)):
    conference = crud.CRUDConference.get(db, conference_id)
    if conference is None:
        raise HTTPException(status_code=404, detail="Conference not found")
    return crud.CRUDConference.delete(db, conference_id)
