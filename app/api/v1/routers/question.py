from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.models import Question
from app.api.v1.schemas import question as schemas
from app.services.database import get_db
from app.services.logging import log_endpoint
from app.services.utils import not_found

router = APIRouter(
    prefix="/question",
    tags=["question"],
    responses={404: {"description": "Not found"}},
)


@router.post(
    "/", response_model=schemas.QuestionSchema, status_code=status.HTTP_201_CREATED
)
@log_endpoint
async def create_question(
    question_in: schemas.QuestionCreateSchema, db: Session = Depends(get_db)
):
    try:
        if await Question.get_by(db, name=question_in.name):
            raise HTTPException(status_code=400, detail="Question already registered")
        return await Question.create(db, **question_in.model_dump())
    except Exception as e:
        raise HTTPException(400, f"Error occured: {e}")


@router.get("/all", response_model=List[schemas.QuestionSchema])
@log_endpoint
async def read_questions(db: Session = Depends(get_db)):
    try:
        return await Question.get_all(db)
    except Exception as e:
        raise HTTPException(400, f"Error occured: {e}")


@router.get("/{question_id}", response_model=schemas.QuestionSchema)
@log_endpoint
async def read_question(question_id: int, db: Session = Depends(get_db)):
    try:
        question = await Question.get(question_id, session=db)
        if not question:
            not_found("Question")
        return schemas.QuestionSchema(**question.__dict__)
    except Exception as e:
        raise HTTPException(400, f"Error occured: {e}")


@router.put("/{question_id}", response_model=schemas.QuestionUpdateSchema)
@log_endpoint
async def update_question(
    question_id: int,
    question_in: schemas.QuestionUpdateSchema,
    db: Session = Depends(get_db),
):
    try:
        question = await Question.get(question_id, session=db)
        if not question:
            not_found("Reservation")
        return await Question.update(db, id=question_id, **question_in.model_dump())
    except Exception as e:
        raise HTTPException(400, f"Error occurred: {e}")


@router.delete("/{question_id}")
@log_endpoint
async def delete_lecture(question_id: int, db: Session = Depends(get_db)):
    try:
        question = await Question.get(question_id, session=db)
        if not question:
            not_found("Reservation")
        await Question.delete(db, id=question_id)
        return question
    except Exception as e:
        raise HTTPException(400, f"Error occurred: {e}")
