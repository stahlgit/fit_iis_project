from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.crud.user import role_required
from app.api.models import Conference, User, UserRole
from app.api.v1.schemas import conference as schemas
from app.services import get_db, log_endpoint, not_found

router = APIRouter(
    prefix="/conferences",
    tags=["conferences"],
    responses={404: {"description": "Not found"}},
)


@router.post(
    "/", response_model=schemas.ConferenceSchema, status_code=status.HTTP_201_CREATED
)
@log_endpoint
async def create_conference(  # ADMIN ONLY
    conference_in: schemas.ConferenceCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(role_required(UserRole.ADMIN)),
) -> schemas.ConferenceSchema:
    try:
        if await Conference.get_by(db, name=conference_in.name):
            raise HTTPException(status_code=400, detail="Conference already registered")
        return await Conference.create(db, **conference_in.model_dump())
    except Exception as e:
        raise HTTPException(400, f"Error occurred: {e}")


@router.get("/all", response_model=List[schemas.ConferenceSchema])  # EVERY USER
@log_endpoint
async def read_conferences(
    db: Session = Depends(get_db),
) -> List[schemas.ConferenceSchema]:
    try:
        return await Conference.get_all(db)
    except Exception as e:
        raise HTTPException(400, f"Error occurred: {e}")


@router.get("/{conference_id}", response_model=schemas.ConferenceSchema)  # EVERY USER
@log_endpoint
async def read_conference(
    conference_id: int, db: Session = Depends(get_db)
) -> schemas.ConferenceSchema:
    try:
        conference = await Conference.get(conference_id, session=db)
        if not conference:
            not_found("Conference")
        return schemas.ConferenceSchema(**conference.__dict__)

    except Exception as e:
        raise HTTPException(400, f"Error occurred: {e}")


@router.put("/{conference_id}", response_model=schemas.ConferenceUpdate)  # ADMIN ONLY
@log_endpoint
async def update_conference(
    conference_id: int,
    conference_in: schemas.ConferenceUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(role_required(UserRole.ADMIN)),
) -> schemas.ConferenceUpdate:
    try:
        conference = await Conference.get(conference_id, session=db)
        if not conference:
            not_found("Conference")
        return await Conference.update(
            db, id=conference_id, **conference_in.model_dump()
        )
    except Exception as e:
        raise HTTPException(400, f"Error occurred: {e}")


@router.delete("/{conference_id}", response_model=schemas.ConferenceSchema)
@log_endpoint
async def delete_conference(  # ADMIN ONLY
    conference_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(role_required(UserRole.ADMIN)),
) -> schemas.ConferenceSchema:
    try:
        conference = await Conference.get(conference_id, session=db)
        if not conference:
            not_found("Conference")
        await Conference.delete(db, id=conference_id)
        return conference
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error occurred: {e}")
