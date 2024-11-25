from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.crud.user import role_required
from app.api.models import GivenPresentation, User, UserRole
from app.api.v1.schemas import given_presentation as schemas
from app.services import check_entities_exist, get_db, log_endpoint, not_found

router = APIRouter(
    prefix="/given_presentation",
    tags=["given_presentation"],
    responses={404: {"description": "Not found"}},
)


@router.post(
    "/",
    response_model=schemas.GivenPresentationCreateSchema,
    status_code=status.HTTP_201_CREATED,
)
@log_endpoint
async def create_given_presentation(
    given_in: schemas.GivenPresentationCreateSchema,
    db: Session = Depends(get_db),
    current_user: User = Depends(role_required(UserRole.REGISTERED)),
) -> schemas.GivenPresentationCreateSchema:
    try:
        await check_entities_exist(
            db,
            {
                "user": [given_in.user_id],
                "conference": [given_in.conference_id],
            },
        )

        return await GivenPresentation.create(db, **given_in.model_dump())
    except Exception as e:
        raise HTTPException(400, f"Error occured: {e}")


@router.get("/all", response_model=List[schemas.GivenPresentationSchema])
@log_endpoint
async def read_given_presentations(
    db: Session = Depends(get_db),
    current_user: User = Depends(role_required(UserRole.REGISTERED)),
) -> List[schemas.GivenPresentationSchema]:
    try:
        return await GivenPresentation.get_all(db)
    except Exception as e:
        raise HTTPException(400, f"Error occured: {e}")


@router.get("/{given_id}", response_model=schemas.GivenPresentationSchema)
@log_endpoint
async def read_given_presentation(
    given_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(role_required(UserRole.REGISTERED)),
) -> schemas.GivenPresentationSchema:
    try:
        given_presentation = await GivenPresentation.get(given_id, session=db)
        if not given_presentation:
            not_found("Given Presentation")
        return schemas.GivenPresentationSchema(**given_presentation.__dict__)

    except Exception as e:
        raise HTTPException(400, f"Error occured: {e}")


@router.patch("/{given_id}", response_model=schemas.GivenPresentationUpdateSchema)
@log_endpoint
async def update_given_presentation(
    given_id: int,
    given_in: schemas.GivenPresentationUpdateSchema,
    db: Session = Depends(get_db),
    current_user: User = Depends(role_required(UserRole.REGISTERED)),
) -> schemas.GivenPresentationUpdateSchema:
    try:
        given_presentation = await GivenPresentation.get(given_id, session=db)
        if not given_presentation:
            not_found("Given Presentation")
        return await GivenPresentation.update(db, id=given_id, **given_in.model_dump())
    except Exception as e:
        raise HTTPException(400, f"Error occurred: {e}")


@router.delete("/{given_id}", response_model=schemas.GivenPresentationSchema)
@log_endpoint
async def delete_given_presentation(
    given_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(role_required(UserRole.REGISTERED)),
) -> schemas.GivenPresentationSchema:
    try:
        given_presentation = await GivenPresentation.get(given_id, session=db)
        if not given_presentation:
            not_found("Given Presentation")
        await GivenPresentation.delete(db, id=given_id)
        return given_presentation
    except Exception as e:
        raise HTTPException(400, f"Error occurred: {e}")
