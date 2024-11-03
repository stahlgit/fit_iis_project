from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.models import Voting
from app.api.v1.schemas import voting as schemas
from app.services.database import get_db
from app.services.utils import not_found

router = APIRouter(
    prefix="/voting",
    tags=["voting"],
    responses={404: {"description": "Not found"}},
)


@router.post(
    "/", response_model=schemas.VotingSchema, status_code=status.HTTP_201_CREATED
)
async def create_voting(
    voting_in: schemas.VotingCreateSchema, db: Session = Depends(get_db)
):
    try:
        if await Voting.get_by(db, name=voting_in.name):
            raise HTTPException(status_code=400, detail="Voting already registered")
        return await Voting.create(db, **voting_in.model_dump())
    except Exception as e:
        raise HTTPException(400, f"Error occured: {e}")


@router.get("/all", response_model=List[schemas.VotingSchema])
async def read_votings(db: Session = Depends(get_db)):
    try:
        return await Voting.get_all(db)
    except Exception as e:
        raise HTTPException(400, f"Error occured: {e}")


@router.get("/{voting_id}", response_model=schemas.VotingSchema)
async def read_voting(voting_id: int, db: Session = Depends(get_db)):
    try:
        voting = Voting.get(voting_id, session=db)
        if not voting:
            not_found("Voting")
        return schemas.VotingSchema(**voting.__dict__)
    except Exception as e:
        raise HTTPException(400, f"Error occured: {e}")


@router.put("/{voting_id}", response_model=schemas.VotingUpdateSchema)
async def update_voting(
    voting_id: int, voting_in: schemas.VotingUpdateSchema, db: Session = Depends(get_db)
):
    try:
        voting = Voting.get(voting_id, session=db)
        if not voting:
            not_found("Voting")
        return await Voting.update(db, id=voting_id, **voting_in.model_dump())
    except Exception as e:
        raise HTTPException(400, f"Error occurred: {e}")


@router.delete("/{voting_id}")
async def delete_voting(voting_id: int, db: Session = Depends(get_db)):
    try:
        voting = Voting.get(voting_id, session=db)
        if not voting:
            not_found("Voting")
        await Voting.delete(db, id=voting_id)
        return voting
    except Exception as e:
        raise HTTPException(400, f"Error occurred: {e}")
