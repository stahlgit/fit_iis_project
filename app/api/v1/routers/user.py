from typing import Annotated, List

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.api.crud import user as crud
from app.api.models import User, UserRole
from app.api.v1.schemas import user as schemas
from app.services import config, get_db, log_endpoint
from app.services.utils import not_found

router = APIRouter(
    prefix="/user",
    tags=["user"],
    responses={404: {"description": "Not found"}},
)


@router.post("/register", response_model=schemas.UserSchema)
@log_endpoint
async def register_user(
    user_in: schemas.UserCreate, db: Session = Depends(get_db)
) -> schemas.UserSchema:
    try:
        if await User.get_by(db, name=user_in.name):
            raise HTTPException(status_code=400, detail="Username already registered")
        if await User.get_by(db, email=user_in.email):
            raise HTTPException(status_code=400, detail="Email already registered")

        user = await crud.register_user(user_in, db)
        if not user:
            raise HTTPException(
                status_code=400, detail="Error occured while creating user"
            )
        return user
    except Exception as e:
        raise HTTPException(400, f"Error occured: {e}")


@router.post("/token", response_model=schemas.Token)
@log_endpoint
async def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)
) -> schemas.Token:
    user = await crud.authenticate_user(form_data.username, form_data.password, db)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = await crud.create_access_token(data={"sub": user.name})
    return schemas.Token(access_token=access_token, token_type="bearer", role=user.role)


@router.get("/me", response_model=schemas.UserSchema)
@log_endpoint
async def read_users_me(
    current_user: Annotated[User, Depends(crud.get_current_active_user)],
):
    return schemas.UserSchema.from_orm(current_user)


@router.post("{/user_id}/", response_model=schemas.UserSchema)
@log_endpoint
async def set_user_role(
    user_id: int,
    new_role: UserRole,
    current_user: User = Depends(crud.role_required(UserRole.ADMIN)),
    db: Session = Depends(get_db),
):
    user = await crud.set_role(user_id, new_role, db)
    if not user:
        raise HTTPException(
            status_code=400, detail="Error occured while setting user role"
        )
    return user


@router.get("/all", response_model=List[schemas.UserSchema])
@log_endpoint
async def get_all_users(
    current_user: User = Depends(crud.role_required(UserRole.ADMIN)),
    db: Session = Depends(get_db),
) -> List[schemas.UserSchema]:
    try:
        return await User.get_all(db)
    except Exception as e:
        raise HTTPException(400, f"Error occurred: {e}")


@router.put("/register_guest", response_model=schemas.UserSchema)
@log_endpoint
async def register_guest(
    user_in: schemas.UserCreate,
    guest_name: str,
    db: Session = Depends(get_db),
):
    try:
        if await User.get_by(db, name=user_in.name):
            raise HTTPException(status_code=400, detail="Username already registered")
        db_user = await User.get_one_by(db, email=user_in.email)
        if db_user:
            if db_user.email == user_in.email and db_user.role == UserRole.GUEST:
                user = await User.get_one_by(db, name=guest_name)
                if not user:
                    not_found("Guest")
                if user.role == UserRole.ADMIN:
                    raise HTTPException(
                        status_code=400, detail="User cannot assign admin"
                    )
                return await User.update(db, id=user.id, **user_in.dict())
            else:
                raise HTTPException(status_code=400, detail="Email already registered")
    except Exception as e:
        raise HTTPException(400, f"Error occured: {e}")


## THIS WILL BE DELETED LATER
@router.post("{user_id}/DEVset_admin", response_model=schemas.UserSchema)
@log_endpoint
async def set_admin(
    user_id: int,
    db: Session = Depends(get_db),
):
    user = await crud.set_role(user_id, UserRole.ADMIN, db)
    if not user:
        raise HTTPException(
            status_code=400, detail="Error occured while setting user role"
        )
    return user
