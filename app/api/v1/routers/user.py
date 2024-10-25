from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.models import User
from app.api.v1.schemas import user as schemas
from app.services.database import get_db
from app.services.utils import not_found

router = APIRouter(
    prefix="/user",
    tags=["user"],
    responses={404: {"description": "Not found"}},
)
