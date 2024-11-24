from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.crud.user import role_required
from app.api.models import Lecture, User, UserRole
from app.api.v1.schemas import lecture as schemas
from app.services import check_entities_exist, get_db, log_endpoint, not_found

router = APIRouter(
    prefix="/lecture",
    tags=["lecture"],
    responses={404: {"description": "Not found"}},
)


@router.post(
    "/", response_model=schemas.LectureSchema, status_code=status.HTTP_201_CREATED
)
@log_endpoint
async def create_lecture(
    lecture_in: schemas.LectureCreateSchema,
    db: Session = Depends(get_db),
    current_user: User = Depends(role_required(UserRole.REGISTERED)),
) -> schemas.LectureSchema:
    try:
        if await Lecture.get_by(db, name=lecture_in.name):
            raise HTTPException(status_code=400, detail="Lecture already registered")

        await check_entities_exist(
            db,
            {
                "room": [lecture_in.room_id],
                "conference": [lecture_in.conference_id],
                "user": [lecture_in.lecturer_id],
            },
        )

        return await Lecture.create(db, **lecture_in.model_dump())
    except Exception as e:
        raise HTTPException(400, f"Error occured: {e}")


@router.get("/all", response_model=List[schemas.LectureSchema])
@log_endpoint
async def read_lectures(
    db: Session = Depends(get_db),
    current_user: User = Depends(role_required(UserRole.REGISTERED)),
) -> List[schemas.LectureSchema]:
    try:
        return await Lecture.get_all(db)
    except Exception as e:
        raise HTTPException(400, f"Error occured: {e}")


@router.get("/{lecture_id}", response_model=schemas.LectureSchema)
@log_endpoint
async def read_lecture(
    lecture_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(role_required(UserRole.REGISTERED)),
) -> schemas.LectureSchema:
    try:
        lecture = await Lecture.get(lecture_id, session=db)
        if not lecture:
            not_found("Lecture")
        return schemas.LectureSchema(**lecture.__dict__)
    except Exception as e:
        raise HTTPException(400, f"Error occured: {e}")


@router.put("/{lecture_id}", response_model=schemas.LectureUpdateSchema)
@log_endpoint
async def update_lecture(
    lecture_id: int,
    lecture_in: schemas.LectureUpdateSchema,
    db: Session = Depends(get_db),
    current_user: User = Depends(role_required(UserRole.REGISTERED)),
) -> schemas.LectureUpdateSchema:
    try:
        lecture = await Lecture.get(lecture_id, sesion=db)
        if not lecture:
            not_found("Lecture")
        return await Lecture.update(db, id=lecture_id, **lecture_in.model_dump())
    except Exception as e:
        raise HTTPException(400, f"Error occurred: {e}")


@router.delete("/{lecture_id}", response_model=schemas.LectureSchema)
@log_endpoint
async def delete_lecture(
    lecture_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(role_required(UserRole.REGISTERED)),
) -> schemas.LectureSchema:
    try:
        lecture = await Lecture.get(lecture_id, sesion=db)
        if not lecture:
            not_found("Lecture")
        await Lecture.delete(db, id=lecture_id)
        return lecture
    except Exception as e:
        raise HTTPException(400, f"Error occurred: {e}")
