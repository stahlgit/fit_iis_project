import datetime
from typing import Optional

from fastapi import Depends, HTTPException, status
from jose import JWTError, jwt
from sqlalchemy.orm import Session

from app.api.models import User
from app.api.v1.schemas.user import UserCreate, UserRoleEnum, UserUpdate
from app.services import config, get_db, get_password_hash, verify_password


async def register_user(user_in: UserCreate, db: Session) -> User:
    hashed_password = get_password_hash(user_in.password)
    new_user = await User.create(
        db, name=user_in.name, email=user_in.email, hashed_password=hashed_password
    )
    if not new_user:
        raise HTTPException(status_code=400, detail="Error while creating user")
    return new_user


async def authenticate_user(
    username: str,
    password: str,
    db: Session = Depends(get_db),
) -> Optional[User]:
    try:
        user = User.get_by(db, name=username)
        ## password je input od usera
        ## hashed password je z DB
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        if not verify_password(password, user.hashed_password):
            raise HTTPException(status_code=400, detail="Incorrect password")
        return user
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error occured: {e}")


async def create_access_token(data: dict) -> str:
    to_encode = data.copy()
    expire = datetime.utcnow() + datetime.timedelta(
        minutes=config.ACCESS_TOKEN_EXPIRE_MINUTES
    )
    to_encode.update({"exp": expire})  # Add expiry to token payload
    return jwt.encode(to_encode, config.SECRET_KEY, algorithm=config.ALGORITHM)


async def get_current_user(
    token: str = Depends(config.oauth2_scheme), db: Session = Depends(get_db)
) -> User:
    try:
        payload = jwt.decode(token, config.SECRET_KEY, algorithms=[config.ALGORITHM])
        user_id = payload.get("sub")
        if user_id is None:
            raise HTTPException(status_code=404, detail="User not found")
        user = User.get_by(db, id=user_id)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        return user
    except JWTError:
        raise HTTPException(status_code=403, detail="Could not validate credentials")
    except Exception as e:
        raise HTTPException(status_code=403, detail=f"Error occured: {e}")


async def get_admin(current_user: User = Depends(get_current_user)) -> User:
    if current_user.role != UserRoleEnum.ADMIN:
        raise HTTPException(status_code=403, detail="Admin access required")
    return current_user
