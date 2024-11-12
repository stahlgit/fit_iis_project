from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.api.crud import user as crud
from app.api.models import User
from app.api.v1.schemas import user as schemas
from app.services import config, get_db, log_endpoint

router = APIRouter(
    prefix="/user",
    tags=["user"],
    responses={404: {"description": "Not found"}},
)


@router.post("/register", response_model=schemas.UserSchema)
@log_endpoint
async def register_user(user_in: schemas.UserCreate, db: Session = Depends(get_db)):
    try:
        if await User.get_by(db, name=user_in.name):
            raise HTTPException(status_code=400, detail="Username already registered")

        user = await crud.register_user(user_in, db)
        if not user:
            raise HTTPException(
                status_code=400, detail="Error occured while creating user"
            )
        return user
    except Exception as e:
        raise HTTPException(400, f"Error occured: {e}")


@router.post("token", response_model=schemas.Token)
@log_endpoint
async def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)
):
    user = await crud.authenticate_user(form_data.username, form_data.password, db)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = await crud.create_access_token(data={"sub": user.id})
    return {"access_token": access_token, "token_type": "bearer"}


@router.get("/me", response_model=schemas.UserSchema)
@log_endpoint
async def read_users_me(current_user: User = Depends(crud.get_current_user)):
    return current_user


@router.post("{/user_id}/   ", response_model=schemas.UserSchema)
@log_endpoint
async def set_user_role(
    user_id: int,
    new_role: schemas.UserRoleEnum,
    admin_user=Depends(crud.get_admin),
    db: Session = Depends(get_db),
):
    if not admin_user:
        raise HTTPException(status_code=401, detail="Admin access required")
    user = await crud.set_user_role(user_id, new_role, db)
    if not user:
        raise HTTPException(
            status_code=400, detail="Error occured while setting user role"
        )
    return user
