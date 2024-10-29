from fastapi import APIRouter, Depends, HTTPException, status
from fastapi_jwt_auth import AuthJWT
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.api.models import User, UserRole
from app.api.v1.schemas import user as schemas
from app.services.config import JWT_SECRET_KEY
from app.services.database import get_db

router = APIRouter()


@router.post("/register", status_code=status.HTTP_201_CREATED)
async def register(user: schemas.UserCreate, db: Session = Depends(get_db)):
    existing_user = await User.get_one_by(name=user.name, email=user.email)
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    new_user = await User.create(session=db, name=user.name, email=user.email)
    new_user.set_password(user.password)
    await db.commit()


@router.post("/login", response_model=schemas.UserRead)
async def login(user: schemas.UserLogin, db: Session = Depends(get_db)):
    user = await User.get_one_by(email=user.email)
    if user is None or not user.check_password(user.password):
        raise HTTPException(status_code=400, detail="Invalid credentials")
    access_token = AuthJWT.create_access_token(subject=user.email)
    return {"access_token": access_token, "token_type": "bearer"}
