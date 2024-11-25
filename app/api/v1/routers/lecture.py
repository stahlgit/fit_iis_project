from typing import List

from fastapi import APIRouter, Depends, HTTPException, UploadFile, status
from sqlalchemy.orm import Session

from app.api.crud import image as image_crud
from app.api.crud.user import role_required
from app.api.models import Lecture, User, UserRole
from app.api.v1 import schemas as schemas
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


@router.get("/conference/{conference_id}", response_model=List[schemas.LectureSchema])
@log_endpoint
async def read_lectures_by_conference(
    conference_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(role_required(UserRole.REGISTERED)),
) -> List[schemas.LectureSchema]:
    try:
        lectures = await Lecture.get_by(db, conference_id=conference_id)
        return [schemas.LectureSchema(**lecture.__dict__) for lecture in lectures]
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


@router.post("/upload")
@log_endpoint
async def upload_lecture_image(
    file: UploadFile,
    lecture_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(role_required(UserRole.REGISTERED)),
):
    try:
        await check_entities_exist(
            db,
            {
                "lecture": [lecture_id],
            },
        )

        lecture = await Lecture.get_one_by(db, id=lecture_id)
        image_filename = image_crud.store_image(file)
        image_path = f"media/images/{image_filename}"

        await lecture.update(db, id=lecture_id, image=image_path)

        return {"path": image_path}
    except schemas.InvalidFileName as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=e.message)


@router.get("/download/{lecture_id}")
async def read_upload_file(
    lecture_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(role_required(UserRole.REGISTERED)),
):
    try:
        await check_entities_exist(
            db,
            {
                "lecture": [lecture_id],
            },
        )
        lecture = await Lecture.get_one_by(db, id=lecture_id)
        filename = lecture.image.split("/")[-1]
        return image_crud.read_image(filename)
    except schemas.InvalidFileName as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=e.message)
