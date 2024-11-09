from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.models import Lecture
from app.api.v1.schemas import lecture as schemas
from app.services import get_db, log_endpoint, not_found

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
    lecture_in: schemas.LectureCreateSchema, db: Session = Depends(get_db)
):
    try:
        if await Lecture.get_by(db, name=lecture_in.name):
            raise HTTPException(status_code=400, detail="Lecture already registered")
        return await Lecture.create(db, **lecture_in.model_dump())
    except Exception as e:
        raise HTTPException(400, f"Error occured: {e}")


@router.get("/all", response_model=List[schemas.LectureSchema])
@log_endpoint
async def read_lectures(db: Session = Depends(get_db)):
    try:
        return await Lecture.get_all(db)
    except Exception as e:
        raise HTTPException(400, f"Error occured: {e}")


@router.get("/{lecture_id}", response_model=schemas.LectureSchema)
@log_endpoint
async def read_lecture(lecture_id: int, db: Session = Depends(get_db)):
    try:
        lecture = await Lecture.get(lecture_id, sesion=db)
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
):
    try:
        lecture = await Lecture.get(lecture_id, sesion=db)
        if not lecture:
            not_found("Lecture")
        return await Lecture.update(db, id=lecture_id, **lecture_in.model_dump())
    except Exception as e:
        raise HTTPException(400, f"Error occurred: {e}")


@router.delete("/{lecture_id}")
@log_endpoint
async def delete_lecture(lecture_id: int, db: Session = Depends(get_db)):
    try:
        lecture = await Lecture.get(lecture_id, sesion=db)
        if not lecture:
            not_found("Lecture")
        await Lecture.delete(db, id=lecture_id)
        return lecture
    except Exception as e:
        raise HTTPException(400, f"Error occurred: {e}")
