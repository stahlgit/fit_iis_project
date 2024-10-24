from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from requests import Session

from app.api.models import GivenPresentation
from app.api.v1.schemas import given_presentation as schemas
from app.services.database import get_db
from app.services.utils import not_found

router = APIRouter(
    prefix="given_presentation",
    tags=["given_presentation"],
    responses={404: {"description": "Not found"}},
)


@router.post(
    "/",
    response_model=schemas.GivenPresentationCreateSchema,
    status_code=status.HTTP_201_CREATED,
)
async def create_given_presentation(
    given_in: schemas.GivenPresentationCreateSchema, db: Session = Depends(get_db)
):
    try:
        return await GivenPresentation.create(db, given_in)
    except Exception as e:
        raise HTTPException(400, f"Error occured: {e}")


@router.get("/all", response_model=List[schemas.GivenPresentationSchema])
async def read_given_presentations(
    skip: int = 0, limi: int = 100, db: Session = Depends(get_db)
):
    try:
        return await GivenPresentation.get_all(db)
    except Exception as e:
        raise HTTPException(400, f"Error occured: {e}")


@router.get("/{given_id}", response_model=schemas.GivenPresentationCreateSchema)
async def read_given_presentation(given_id: int, db: Session = Depends(get_db)):
    try:
        given_presentation = GivenPresentation.get(db, id=given_id)
        return await given_presentation
    except given_presentation.DoesNotExist:
        not_found("Given Presentation")
    except Exception as e:
        raise HTTPException(400, f"Error occured: {e}")


@router.put("/{given_id}", response_model=schemas.GivenPresentationUpdateSchema)
async def update_given_presentation(
    given_id: int,
    given_in: schemas.GivenPresentationUpdateSchema,
    db: Session = Depends(get_db),
):
    try:
        given_presentation = GivenPresentation.get(db, id=given_id)
        if given_presentation is None:
            not_found("Given Presentation")
        return await GivenPresentation.update(db, id=given_id, **given_in.model_dump())
    except Exception as e:
        raise HTTPException(400, f"Error occurred: {e}")


@router.delete("/{given_id}")
async def delete_given_presentation(given_id: int, db: Session = Depends(get_db)):
    try:
        given_presentation = await GivenPresentation.get(db, id=given_id)
        if given_presentation is None:
            not_found("Given Presentation")
        await GivenPresentation.delete(db, id=given_id)
        return given_presentation
    except Exception as e:
        raise HTTPException(400, f"Error occurred: {e}")
