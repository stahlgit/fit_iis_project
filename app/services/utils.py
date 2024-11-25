from datetime import datetime, timedelta

from fastapi import HTTPException
from jose import JWTError, jwt
from passlib.context import CryptContext
from sqlalchemy.orm import Session

from app.api import models

from .config import config


def not_found(model: str):
    raise HTTPException(status_code=404, detail=f"{model} not found")


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)


async def check_entities_exist(db: Session, entity_checks: dict[str, list[int]]):
    entities_dic = {
        "room": models.Room.get_one_by,
        "conference": models.Conference.get_one_by,
        "lecture": models.Lecture.get_one_by,
        "user": models.User.get_one_by,
        "reservation": models.Reservation.get_one_by,
    }
    for entity_type, ids in entity_checks.items():
        for id in ids:
            exists = await entities_dic[entity_type](db, id=id)
            if not exists:
                raise not_found(entity_type.capitalize())
