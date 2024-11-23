from datetime import datetime, timedelta
from typing import Annotated, Optional

from fastapi import Depends, HTTPException, status
from jose import JWTError, jwt
from sqlalchemy.orm import Session

from app.api.models import User, UserRole
from app.api.v1.schemas.user import TokenData, UserCreate, UserUpdate
from app.services import (
    config,
    get_db,
    get_password_hash,
    oauth2_scheme,
    verify_password,
)
from app.services.utils import not_found


async def register_user(user_in: UserCreate, db: Session) -> User:
    hashed_password = get_password_hash(user_in.password)
    new_user = await User.create(
        db,
        name=user_in.name,
        email=user_in.email,
        hashed_password=hashed_password,
        role=UserRole.REGISTERED,
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
        user = await User.get_one_by(db, email=username)
        ## password je input od usera
        ## hashed password je z DB
        if not user:
            not_found("User")
        if not verify_password(password, user.hashed_password):
            raise HTTPException(status_code=400, detail="Incorrect password")
        return user
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error occured: {e}")


async def create_access_token(data: dict) -> str:
    to_encode = data.copy()
    expire = datetime.now() + timedelta(minutes=config.ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, config.JWT_SECRET_KEY, algorithm=config.ALGORITHM)


async def get_current_user(
    token: Annotated[str, Depends(oauth2_scheme)], db: Session = Depends(get_db)
) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(
            token, config.JWT_SECRET_KEY, algorithms=[config.ALGORITHM]
        )
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    user = await User.get_one_by(db, name=username)
    if user is None:
        raise credentials_exception
    return user


async def get_current_active_user(
    current_user: Annotated[User, Depends(get_current_user)],
):
    # if current_user.is_active == False:
    # raise HTTPException(status_code=400, detail="Inactive user")
    return current_user


async def set_role(
    user_id: int, new_role: UserRole, db: Session = Depends(get_db)
) -> User:
    user = await User.get_by(db, id=user_id)
    if not user:
        not_found("User")
    return await User.update(db, id=user_id, role=new_role)


def role_required(required_role: UserRole):
    async def role_checker(current_user: User = Depends(get_current_user)):
        ## ak je admin, tak moze robit vsetko
        if current_user.role == UserRole.ADMIN:
            return current_user

        if current_user.role != required_role:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Operation not permitted",
            )
        return current_user

    return role_checker
